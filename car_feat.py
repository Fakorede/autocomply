# first install package with 
# pip install git+https://github.com/appknox/pyaxmlparser.git
# pip install androguard==3.3.5

import sys
from androguard.core.bytecodes.apk import APK
from xml.etree import ElementTree
from pyaxmlparser.axmlprinter import AXMLPrinter

def get_manifest_xml(apk_path):
    # Load the APK file
    apk = APK(apk_path)
    
    # Extract and return the AndroidManifest.xml as a string
    return apk.get_android_manifest_xml()

def check_android_auto_support(root):
    try:
        # Find <meta-data> tag with name="com.google.android.gms.car.application"
        auto_support = False
        for meta_data in root.findall(".//meta-data"):
            name = meta_data.attrib.get('{http://schemas.android.com/apk/res/android}name')
            if len(name) and name == 'com.google.android.gms.car.application':
                auto_support = True
                break
        return auto_support
    except:
        print()

def get_auto_capabilities(apk_path):
    # Load the APK file
    apk = APK(apk_path)

    xml_file = None
    try:
        xml_file = apk.get_file("res/xml/automotive_app_desc.xml")
    except Exception as e:
        print("❓ File not found:", e)
        return

    
    # Parse the automotive_app_desc.xml to find supported capabilities
    if xml_file:
        try:
            axml = AXMLPrinter(xml_file).get_xml()
            root = ElementTree.fromstring(axml)
            capabilities = []
            for use in root.findall("uses"):
                capabilities.append(use.attrib.get('name').upper())
            return capabilities
        except Exception as e:
            print("Failed to parse xml content:", e)
            return []
    else:
        print("No automotive XML content found or failed to extract.")
        return []
    
def check_app_categories(root):
    try:
        # Find <service> tags and their <intent-filter> sub-tags
        categories = []
        for service in root.findall(".//service"):
            intent_filters = service.findall(".//intent-filter")
            for intent_filter in intent_filters:
                category_elements = intent_filter.findall(".//category")
                for category in category_elements:
                    category_name = category.attrib.get('{http://schemas.android.com/apk/res/android}name')
                    if len(category_name) and category_name.startswith("androidx.car.app.category."):
                        categories.append(category_name)
        return categories
    except Exception as e:
        print("❓ Error checking app categories:", e)
        return []
    
def check_min_car_api_level(root):
    try:
        # Find <meta-data> tag with name="androidx.car.app.minCarApiLevel"
        min_car_api_level = None
        for meta_data in root.findall(".//meta-data"):
            name = meta_data.attrib.get('{http://schemas.android.com/apk/res/android}name')
            if len(name) and name == 'androidx.car.app.minCarApiLevel':
                min_car_api_level = meta_data.attrib.get('{http://schemas.android.com/apk/res/android}value')
                break
        return min_car_api_level
    except Exception as e:
        print("❓ Error checking minCarApiLevel:", e)
        return None

def detect_auto_capabilities(apk_path, apk_category, root):
    # Check if the APK supports Android Auto
    auto_support = check_android_auto_support(root)
    
    if not auto_support:
        print("❌ This APK does not support Android Auto.")
        return
    
    print(f"✅ Android Auto is supported.")

    if apk_category in ["poi", "navigation"]:
        # Check the minimum Car App API level
        min_car_api_level = check_min_car_api_level(root)
        if min_car_api_level:
            print(f"✅ Minimum Car App API Level declared: {min_car_api_level}")
        else:
            print("❌ No minimum Car App API Level detected.")
    
    # Get the auto capabilities
    capabilities = get_auto_capabilities(apk_path)

    if capabilities and apk_category in ["poi", "navigation"]:
        if 'TEMPLATE' in capabilities:
            print(capabilities)
            print("✅ The APK supports the 'template' capability (to be declared for 'Android for Cars App Library').")
            categories = check_app_categories(root)
            print(f"✅ Supported Android Auto category: {', '.join(categories)}")
        else:
            print("❗ The 'template' capability (to be declared for 'Android for Cars App Library') is not supported.")
            print(f"✅ Supported Android Auto category: {', '.join(capabilities)}")
    else:
        categories = check_app_categories(root)
        if categories:
            print(f"✅ Supported Android Auto category: {', '.join(categories)}")
        else:
            print("❌ No specific Android Auto capabilities detected.")

def check_media_browser_service(root):
    """
    Check for the MediaBrowserService.
    :param root: AndroidManifest xml elements.
    :return: the presence of a declared intent for MediaBrowserService, and the android service. 
    """
    try:
        # Find <service> tag with an <intent-filter> that has <action> with name=="android.media.browse.MediaBrowserService"
        media_intent_filter = False
        service_name = None
        service_exported = False

        for service in root.findall(".//service"):
            intent_filters = service.findall(".//intent-filter")
            for intent_filter in intent_filters:
                actions = intent_filter.findall(".//action")
                for action in actions:
                    action_name = action.attrib.get('{http://schemas.android.com/apk/res/android}name')
                    if len(action_name) and action_name == "android.media.browse.MediaBrowserService":
                        service_name = service.attrib.get('{http://schemas.android.com/apk/res/android}name')
                        service_exported = service.attrib.get('{http://schemas.android.com/apk/res/android}exported')
                        media_intent_filter = True
        return (service_name, service_exported, media_intent_filter)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def find_media_search_intent(root):
    """
    Find if either the main activity or a MediaBrowserService has the MEDIA_PLAY_FROM_SEARCH intent filter.
    
    Args:
        root: ElementTree root element of AndroidManifest.xml
        
    Returns:
        bool: True if MEDIA_PLAY_FROM_SEARCH intent filter is found in either location
    """
    ANDROID_NS = '{http://schemas.android.com/apk/res/android}'
    
    try:
        found_in_activity = False
        found_in_service = False
        
        # Check main activity
        for activity in root.findall(".//activity"):
            intent_filters = activity.findall(".//intent-filter")
            for intent_filter in intent_filters:
                has_main = False
                has_launcher = False
                has_default = False
                
                # Check for MAIN action
                actions = intent_filter.findall(".//action")
                for action in actions:
                    if action.attrib.get(f'{ANDROID_NS}name') == "android.intent.action.MAIN":
                        has_main = True
                        break
                
                # Check for LAUNCHER category
                categories = intent_filter.findall(".//category")
                for category in categories:
                    if category.attrib.get(f'{ANDROID_NS}name') == "android.intent.category.LAUNCHER":
                        has_launcher = True
                        break

                # Check for DEFAULT category
                categories = intent_filter.findall(".//category")
                for category in categories:
                    if category.attrib.get(f'{ANDROID_NS}name') == "android.intent.category.DEFAULT":
                        has_default = True
                        break
                
                # If this is the main activity, check for MEDIA_PLAY_FROM_SEARCH
                if (has_main and has_launcher) or has_default:
                    for intent_filter in activity.findall(".//intent-filter"):
                        actions = intent_filter.findall(".//action")
                        for action in actions:
                            action_name = action.attrib.get(f'{ANDROID_NS}name')
                            if action_name == "android.media.action.MEDIA_PLAY_FROM_SEARCH":
                                found_in_activity = True
                                break
                    break

        if found_in_activity:
            return True
        
        # First find the service with MediaBrowserService
        media_browser_service = None
        for service in root.findall(".//service"):
            intent_filters = service.findall(".//intent-filter")
            for intent_filter in intent_filters:
                actions = intent_filter.findall(".//action")
                for action in actions:
                    action_name = action.attrib.get(f'{ANDROID_NS}name')
                    if action_name == "android.media.browse.MediaBrowserService":
                        media_browser_service = service
                        break
                if media_browser_service is not None:
                    break
            if media_browser_service is not None:
                break
        
        # If we found the MediaBrowserService, check it for MEDIA_PLAY_FROM_SEARCH
        if media_browser_service is not None:
            for intent_filter in media_browser_service.findall(".//intent-filter"):
                actions = intent_filter.findall(".//action")
                for action in actions:
                    action_name = action.attrib.get(f'{ANDROID_NS}name')
                    if action_name == "android.media.action.MEDIA_PLAY_FROM_SEARCH":
                        found_in_service = True
    
        
        return found_in_activity or found_in_service
        
    except Exception as e:
        print(f"Error parsing manifest: {str(e)}")
        return False

def check_media_actions(root):
    """
    
    :param root: AndroidManifest xml elements.
    :return: service_name.
    """
    try:
        # check if media browser service is declared
        service_name, service_exported, media_intent_filter  = check_media_browser_service(root)

        if media_intent_filter:
            print("✓ 'MediaBrowserService' has been properly declared in manifest file.")
        else:
            print("✗ 'MediaBrowserService' NOT properly declared, see https://developer.android.com/training/cars/media#manifest-service.")

        if service_exported:
            print("✓ Media Service has been exported.")
        else:
            print("✗ Media Service NOT exported. see https://developer.android.com/training/cars/media#manifest-service")

        # play_from_search
        if find_media_search_intent(root):
            print("✓ 'MEDIA_PLAY_FROM_SEARCH' has been properly declared in manifest file.")
        else:
            print("✗ 'MEDIA_PLAY_FROM_SEARCH' NOT declared.")

        # return media service name if found
        if service_name:
            return service_name
        else:
            print("✗ Media Service NOT detected.")
            return None
    except Exception as e:
        print("❓ Error checking media service:", e)
        return None

def find_poi_service(root):
    """
    Check for the poi service.
    :param root: AndroidManifest xml elements.
    :return: the presence of a declared service for poi servce. 
    """
    try:
        # Find <service> tag with an <intent-filter> that has <action> and <category>"
        poi_intent_action = False
        poi_intent_category = False
        service_name = None
        service_exported = False

        poi_action_name  = "androidx.car.app.CarAppService"
        poi_category_name = "androidx.car.app.category.POI"
        parking_category_name = "androidx.car.app.category.PARKING"
        charging_category_name = "androidx.car.app.category.CHARGING"
        deprecated_category = False
        for service in root.findall(".//service"):
            intent_filters = service.findall(".//intent-filter")
            for intent_filter in intent_filters:
                actions = intent_filter.findall(".//action")
                for action in actions:
                    action_name = action.attrib.get('{http://schemas.android.com/apk/res/android}name')
                    if len(action_name) and action_name == poi_action_name:
                        poi_intent_action = True
                        service_name = service.attrib.get('{http://schemas.android.com/apk/res/android}name')
                        service_exported = service.attrib.get('{http://schemas.android.com/apk/res/android}exported')
                categories = intent_filter.findall(".//category")
                for category in categories:
                    category_name = category.attrib.get('{http://schemas.android.com/apk/res/android}name')
                    if len(category_name) and category_name == poi_category_name:
                        poi_intent_category = True
                    if len(category_name) and (category_name == charging_category_name or category_name == parking_category_name):
                        poi_intent_category = True
                        deprecated_category = True
                # we don't wana search any other <intent-filter> and overwrite the results
                if poi_intent_action or poi_intent_category:break
            
        return (service_name, service_exported, poi_intent_action, poi_intent_category, deprecated_category)
    except Exception as e:
        print("❓ Error checking for poi service in manifest:", e)
        return None

def find_templates_permission(root, template):
    """
    Check manfest for templates.
    :param root: AndroidManifest xml elements.
    :return: True if <uses-permission> is found, or False otherwise.
    """
    try:
        # Find <uses-permission> tag that requests permission for TEMPLATES
        templates_permission = False

        for permission in root.findall(".//uses-permission"):
            if template == permission.attrib.get('{http://schemas.android.com/apk/res/android}name'):
                templates_permission = True

        return templates_permission
    except Exception as e:
        print("❓ Error checking for templates permission:", e)
        return None


def check_poi_actions(root):
    """
    
    :param root: AndroidManifest xml elements.
    :return: service_name.
    """
    try:
        # check if CarAppService is declared
        service_name, service_exported, poi_intent_action, poi_intent_category, deprecated_category  = find_poi_service(root)

        if poi_intent_action:
            print("✅ 'CarAppService' has been properly declared in manifest file.")
        else:
            print("❌ 'CarAppService' NOT properly declared, see https://developer.android.com/training/cars/apps/poi#declare-poi-support.")
        
        if poi_intent_category:
            print("✅ POI category has been properly declared in manifest file.")
        else:
            print("❌ POI category NOT properly declared, see https://developer.android.com/training/cars/apps/poi#declare-poi-support.")

        if deprecated_category:
            print("Uses a deprecated category i.e. parking or charging")

        if service_exported:
            print("✅ Poi Service has been exported.")
        else:
            print("❌ Poi Service NOT exported. see https://developer.android.com/training/cars/apps/poi#declare-poi-support")

        # map templates
        if find_templates_permission(root, "androidx.car.app.MAP_TEMPLATES"):
            print("✅ 'MAP_TEMPLATES' permission has been requested in manifest file.")
        else:
            print("❌ 'MAP_TEMPLATES' permission NOT requested.")

        # return poi service name if found
        if service_name:
            return service_name
        else:
            print("❌ POI Service NOT detected.")
            return None
    except Exception as e:
        print("❓ Error checking poi service:", e)
        return None


def find_navigation_service(root):
    """
    Check for the navigation service.
    :param root: AndroidManifest xml elements.
    :return: the presence of a declared service for poi servce. 
    """
    try:
        # Find <service> tag with an <intent-filter> that has <action> and <category>"
        navigation_intent_action = False
        navigation_intent_category = False
        service_name = None
        service_exported = False
        navigation_action_name  = "androidx.car.app.CarAppService"
        navigation_category_name = "androidx.car.app.category.NAVIGATION"

        for service in root.findall(".//service"):
            for intent_filter in service.findall(".//intent-filter"):
                actions = intent_filter.findall(".//action")
                for action in actions:
                    action_name = action.attrib.get('{http://schemas.android.com/apk/res/android}name')
                    if len(action_name) and action_name == navigation_action_name:
                        navigation_intent_action = True
                        service_name = service.attrib.get('{http://schemas.android.com/apk/res/android}name')
                        service_exported = service.attrib.get('{http://schemas.android.com/apk/res/android}exported')
                categories = intent_filter.findall(".//category")
                for category in categories:
                    category_name = category.attrib.get('{http://schemas.android.com/apk/res/android}name')
                    if len(category_name) and category_name == navigation_category_name:
                        navigation_intent_category = True
                # we don't wana search any other <intent-filter> and overwrite the results
                if navigation_intent_action or navigation_intent_category:break
            
        return (service_name, service_exported, navigation_intent_action, navigation_intent_category)
    except Exception as e:
        print("❓ Error checking for navigation service in manifest:", e)
        return None


def check_navigation_actions(root):
    """
    
    :param root: AndroidManifest xml elements.
    :return: service_name.
    """
    try: 
        # check if CarAppService is declared
        service_name, service_exported, navigation_intent_service, navigation_intent_category = find_navigation_service(root)

        if navigation_intent_service:
            print("✓ 'CarAppService' has been properly declared in manifest file.")
        else:
            print("❌ 'CarAppService' NOT properly declared, see https://developer.android.com/training/cars/apps/navigation#declare-navigation-support.")
        if navigation_intent_category:
            print("✓ Navigation category has been properly declared in manifest file.")
        else:
            print("❌ Navigation category NOT properly declared, see https://developer.android.com/training/cars/apps/navigation#declare-navigation-support.")
        if service_exported:
            print("✓ Navigation Service has been exported.")
        else:
            print("❌ Navigation Service NOT exported. see https://developer.android.com/training/cars/apps/navigation#declare-navigation-support")
    
        # navigation templates
        if find_templates_permission(root, "androidx.car.app.NAVIGATION_TEMPLATES"):
            print("✓ 'NAVIGATION_TEMPLATES' permission has been requested in manifest file.")
        else:
            print("❌ 'NAVIGATION_TEMPLATES' permission NOT requested.")

        # return navigation service, if found
        if service_name:
            return service_name
        else:
            print("❌ Navigation service NOT detected.")
        return None
    except Exception as e:
        print("❓ Error checking navigation service:", e)
        return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 manifest_checker.py <apk_path>")
        sys.exit(1)

    apk_path = sys.argv[1]

    # Parse the AndroidManifest.xml
    manifest_xml = get_manifest_xml(apk_path)
    root = manifest_xml.getroottree().getroot()

    # perform manifest checks for media
    media_service_name = check_media_actions(root)
    print(f'MediaService: {media_service_name}')


main()

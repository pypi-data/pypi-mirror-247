import os_xml_handler.xml_handler as xh
from os_xml_automation import shared_tools as shared_tools
from os_android_app_automation.bp import _res as res
import os_file_handler.file_handler as fh
import os
from os_file_stream_handler import file_stream_handler as fsh
import os_android_package_name_changer.name_changer as nc
import os_tools.logger_handler as lh
from os_android_app_automation.bp import _build_gradle_setter


# manipulate an xcode project by an xml properties file
def set_app_name(project_path, app_name):
    strings_path = os.path.join(project_path, res.PROJECT_STRINGS_FILE)
    strings_xml = xh.read_xml_file(strings_path)
    name_node = xh.get_child_nodes(xh.get_root_node(strings_xml), 'string', 'name', 'app_name')[0]
    xh.set_node_text(name_node, app_name)
    xh.save_xml_file(strings_xml, strings_path)


def set_launcher_icons(project_main, launchers_path):
    launcher_icons = fh.search_file(project_main, prefix='ic_launcher', recursive=True)
    fh.remove_files(launcher_icons)
    fh.copy_dir(launchers_path, project_main)


def set_assets(project_assets, assets_path):
    fh.remove_dir(project_assets)
    fh.copy_dir_with_permission_denied(assets_path, project_assets)


# will set the app id in the manifest
def set_ad_id(project_manifest, app_ad_id):
    namespace_map = {'android': 'http://schemas.android.com/apk/res/android'}
    manifest_xml = xh.read_xml_file(project_manifest, namespace_map)
    application_node = xh.get_child_nodes(xh.get_root_node(manifest_xml), 'application')[0]
    ad_node = xh.get_child_nodes(application_node, 'meta-data', 'android:name', 'com.google.android.gms.ads.APPLICATION_ID', namespace_map)
    if ad_node:
        xh.set_node_atts(ad_node[0], {'android:value': app_ad_id}, namespace_map=namespace_map)
    else:
        xh.create_and_add_new_node(application_node,
                                   'meta-data',
                                   {'android:name': 'com.google.android.gms.ads.APPLICATION_ID',
                                    'android:value': app_ad_id},
                                   namespace_map=namespace_map)

    xh.save_xml_file(manifest_xml, project_manifest, add_utf_8_encoding=True)


def get_old_package_name(project_path, project_manifest):
    # try to get package name from the manifest
    manifest_xml = xh.read_xml_file(project_manifest)
    root_node = xh.get_root_node(manifest_xml)
    package_name = xh.get_node_att(root_node, 'package')
    if not package_name:  # try from build.gradle
        build_gradle = os.path.join(project_path, 'app', 'build.gradle')
        build_gradle_lines = fsh.read_text_file(build_gradle)
        for line in build_gradle_lines:
            line = str(line).strip()
            if line.startswith('applicationId'):
                package_name = line.replace('applicationId', '').strip().replace("\"", "").replace("'", "")
                break

    if not package_name:
        raise Exception("Error: Couldn't find package name in manifest.xml nor in build.gradle")

    return package_name


# will set the modules list in the project
def set_modules(project_path, added_modules, included_projects, package_name):
    settings_gradle_file = fh.search_file(project_path, 'settings.gradle')[0]
    added_modules_str = '\n'.join([f"include ':{x}'" for x in added_modules])
    # added_modules_str = "\n".join(added_modules)
    root_project_name = package_name.split('.')[-1]
    app_line = "include ':app'"
    last_line = f'rootProject.name = "{root_project_name}"'
    whole_content = f'{added_modules_str}\n{app_line}\n{last_line}'
    for included_project in included_projects:
        whole_content += f"\ninclude ':{included_project['project_name']}'"
        whole_content += f"\nproject(':{included_project['project_name']}').projectDir = new File('{included_project['project_dir']}')"

    fsh.write_file(settings_gradle_file, whole_content)


def manipulate(xml_path, xml, place_holder_map, on_backup, on_pre_build):
    logger = lh.Logger(name="[App Automation]")
    root_node = xh.get_root_node(xml)

    xml = shared_tools.add_extension_nodes(xml_path, place_holder_map, root_node, xml)
    root_node = xh.get_root_node(xml)

    # fetch the settings nodes
    settings_node = xh.get_child_nodes(root_node, 'settings')[0]
    create_alias = xh.get_text_from_child_node(settings_node, 'work_on_project_alias')
    create_alias = shared_tools.fill_place_holders(create_alias, place_holder_map)

    # fetch the project properties
    project_properties_node = xh.get_child_nodes(root_node, 'project_properties')[0]

    # project path
    project_path = xh.get_text_from_child_node(project_properties_node, 'project_path')
    project_path = shared_tools.fill_place_holders(project_path, place_holder_map)

    # launcher
    launchers_path = xh.get_text_from_child_node(project_properties_node, 'launchers_path')
    launchers_path = shared_tools.fill_place_holders(launchers_path, place_holder_map)

    # assets
    assets_path = xh.get_text_from_child_node(project_properties_node, 'assets_path')
    if assets_path is not None:
        assets_path = shared_tools.fill_place_holders(assets_path, place_holder_map)

    # google services
    google_services_path = xh.get_text_from_child_node(project_properties_node, 'google_services_path')
    if google_services_path:
        google_services_path = shared_tools.fill_place_holders(google_services_path, place_holder_map)

    # all of the other props
    package_name = xh.get_text_from_child_node(project_properties_node, 'package_name')

    # version name
    version_name = xh.get_text_from_child_node(project_properties_node, res.VERSION_NAME)
    version_name = shared_tools.fill_place_holders(version_name, place_holder_map)

    # version code
    version_code = xh.get_text_from_child_node(project_properties_node, res.VERSION_CODE)
    version_code = shared_tools.fill_place_holders(version_code, place_holder_map)

    app_ad_id = xh.get_text_from_child_node(project_properties_node, 'app_ad_id')
    app_name = xh.get_text_from_child_node(project_properties_node, 'app_name')

    # will set the version name and code on the original project
    _build_gradle_setter.set_versions(project_path, logger, version_name, version_code)

    # alias creation
    if create_alias.lower() == 'true':
        alias_path = f'{project_path}_alias'
        fh.remove_dir(alias_path)
        logger.info(f'Creating project alias directory ({alias_path})...')
        fh.copy_dir(project_path, alias_path)
        project_path = alias_path
        place_holder_map["$project_path"] = project_path

    # build paths
    project_app = os.path.join(project_path, res.PROJECT_APP)
    project_main = os.path.join(project_path, res.PROJECT_MAIN)
    project_assets = os.path.join(project_path, res.PROJECT_ASSETS_DIR)
    project_build_gradle = os.path.join(project_path, res.PROJECT_BUILD_GRADLE_FILE)
    project_manifest = os.path.join(project_path, res.PROJECT_MANIFEST)
    old_package_name = get_old_package_name(project_path, project_manifest)

    # do backup
    logger.info('running on_backup...')
    if on_backup is not None:
        on_backup(project_path, old_package_name, package_name, place_holder_map)

    # set the general properties in the android project
    logger.info('setting general properties...')
    set_app_name(project_path, app_name)
    set_launcher_icons(project_main, launchers_path)
    if assets_path is not None:
        set_assets(project_assets, assets_path)

    # set ad id in manifest
    if app_ad_id:
        set_ad_id(project_manifest, app_ad_id)

        # add dependencies
    logger.info('adding dependencies...')
    dependencies_nodes = xh.get_child_nodes(root_node, 'gradle_dependencies')
    if dependencies_nodes:
        _build_gradle_setter.set_dependencies(project_build_gradle, dependencies_nodes)

    # add modules
    added_modules_node = xh.get_child_nodes(root_node, 'added_modules')
    included_modules = []
    included_projects = []
    if added_modules_node:
        for include_node in xh.get_child_nodes(added_modules_node[0], 'include'):
            included_modules.append(xh.get_text_from_node(include_node))
        for added_project in xh.get_child_nodes(added_modules_node[0], 'project'):
            project_name = xh.get_text_from_node(added_project)
            project_dir = xh.get_node_att(added_project, 'projectDir')
            included_projects.append({'project_name': project_name, 'project_dir': project_dir})

    logger.info('setting modules...')
    set_modules(project_path, included_modules, included_projects, package_name)

    logger.info('running package name changer...')
    nc.change_package_name(project_path, package_name)

    if google_services_path:
        dst = os.path.join(project_app, fh.get_file_name_from_path(google_services_path))
        logger.info('Injecting google_services.json file...')
        logger.info('From ' + google_services_path + ' to ' + dst)
        fh.copy_file(google_services_path, dst)

    # do pre build callback
    logger.info('running on_pre_build...')
    if on_pre_build is not None:
        on_pre_build(project_path, package_name, place_holder_map)


def print_line():
    print('-----------------------------------------------------------------------')

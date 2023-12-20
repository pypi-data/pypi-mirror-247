import { ISettingRegistry } from '@jupyterlab/settingregistry';

export function loadSetting(setting: ISettingRegistry.ISettings): string {
    // Read the settings and convert to the correct type
    let atlasId = setting.get('atlasId-smce').composite as string;
    return atlasId;
}

export async function saveSetting(setting: ISettingRegistry.ISettings, atlasId: string): Promise<string> {
    // Read the settings and convert to the correct type
    await setting.set('atlasId-smce', atlasId);
    return atlasId;
}
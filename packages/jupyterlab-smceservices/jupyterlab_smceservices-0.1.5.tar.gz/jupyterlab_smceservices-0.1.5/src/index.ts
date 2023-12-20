import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IMainMenu } from '@jupyterlab/mainmenu';
import { Dialog, MainAreaWidget, showDialog } from '@jupyterlab/apputils';
import { ILauncher } from "@jupyterlab/launcher";
import { Menu } from '@lumino/widgets';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ChatlasWidget } from './widgets/ChatlasWidget';
import { aboutVoiceAtlasDialog } from './widgets/AboutWidget';
import { loadSetting, saveSetting } from './utils';
import { smceServicesIcon } from './style/IconsStyle'

const PLUGIN_ID = 'jupyterlab_smceservices:plugin';
let atlasId = '';

const plugin: JupyterFrontEndPlugin<void> = {
    id: PLUGIN_ID,
    autoStart: true,
    optional: [IMainMenu, ISettingRegistry, ILauncher],
    activate: activate
};

async function activate(app: JupyterFrontEnd, mainMenu: IMainMenu, settings: ISettingRegistry, launcher: ILauncher): Promise<void> {
    console.log('JupyterLab extension jupyterlab_smceservices is activated!');
    const openChatlas = 'jupyterlab_smceservices:openChatlas';
    const aboutVoiceAtlas = 'jupyterlab_smceservices:aboutVoiceAtlas';

    Promise.all([app.restored, settings.load(PLUGIN_ID)])
        .then(async ([, setting]) => {
            await saveSetting(setting, '59e9d968-9c6a-45b3-aa07-cbdc5207e406')
            atlasId = loadSetting(setting);
        }).catch((reason) => {
            console.error(
                `Something went wrong when changing the settings.\n${reason}`
            );
        });

    const menu = new Menu({ commands: app.commands });
    menu.title.label = 'Support'

    app.commands.addCommand(openChatlas, {
        label: 'Get Support',
        caption: 'Get Support',
        icon: (args) => (args["isPalette"] ? undefined : smceServicesIcon),
        execute: async () => {
            const content = new ChatlasWidget(atlasId)
            content.title.label = 'Get Support';
            // const widget = new MainAreaWidget<VoiceAtlasWidget>({ content })
            const widget = new MainAreaWidget<ChatlasWidget>({ content })
            app.shell.add(widget, 'main');
        }
    });

    app.commands.addCommand(aboutVoiceAtlas, {
        label: 'About Voice Atlas',
        caption: 'About Voice Atlas',
        execute: async () => {
            const { aboutBody, aboutTitle } = aboutVoiceAtlasDialog();
            const result = await showDialog({
                title: aboutTitle,
                body: aboutBody,
                buttons: [
                    Dialog.createButton({
                        label: 'Dismiss',
                        className: 'jp-About-button jp-mod-reject jp-mod-styled'
                    })
                ]
            });

            if (result.button.accept) {
                return;
            }
        }
    })

    menu.addItem({ command: openChatlas });
    menu.addItem({ type: 'separator' });
    menu.addItem({
        command: aboutVoiceAtlas,
        args: { origin: 'from menu' },
    });

    mainMenu.addMenu(menu, true, { rank: 2000 });

    if (launcher) {
        launcher.add({
            command: openChatlas,
            category: "Support",
            args: { isLauncher: true }
        });
    }
}

export default plugin;

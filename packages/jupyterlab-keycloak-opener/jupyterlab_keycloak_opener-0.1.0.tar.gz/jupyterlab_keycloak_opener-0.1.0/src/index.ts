import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { ILauncher } from '@jupyterlab/launcher';
import { usersIcon } from '@jupyterlab/ui-components';

const PALETTE_CATEGORY = 'Admin tools';
namespace CommandIDs {
  export const createNew = 'jupyterlab-keycloak-opener:open-keycloak-console';
}

/**
 * Initialization data for the jupyterlab-keycloak-opener extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-keycloak-opener:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  optional: [ILauncher, ICommandPalette],
  activate: (
    app: JupyterFrontEnd,
    launcher: ILauncher | null,
    palette: ICommandPalette | null
  ) => {
    console.log(
      'JupyterLab extension jupyterlab-keycloak-opener is activated!'
    );

    const { commands } = app;
    const command = CommandIDs.createNew;

    commands.addCommand(command, {
      label: 'Users',
      caption: 'Users',
      icon: args => (args['isPalette'] ? undefined : usersIcon),
      execute: async args => {
        window.open(
          'https://auth.opensciencestudio.com/admin/Navteca/console',
          '_blank',
          'noreferrer'
        );
      }
    });

    if (launcher) {
      launcher.add({
        command,
        category: 'Admin tools',
        rank: 1
      });
    }

    if (palette) {
      palette.addItem({
        command,
        args: { isPalette: true },
        category: PALETTE_CATEGORY
      });
    }
  }
};

export default plugin;

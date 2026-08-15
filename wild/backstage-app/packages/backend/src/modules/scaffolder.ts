import { createBackendModule } from '@backstage/backend-plugin-api';
import { scaffolderActionsExtensionPoint } from '@backstage/plugin-scaffolder-node';
import { createCustomAction } from './custom-action';

export const scaffolderModuleCustomAction = createBackendModule({
  pluginId: 'scaffolder',
  moduleId: 'custom-action',
  register(env) {
    env.registerInit({
      deps: {
        scaffolder: scaffolderActionsExtensionPoint,
      },
      async init({ scaffolder }) {
        scaffolder.addActions(createCustomAction());
      },
    });
  },
});
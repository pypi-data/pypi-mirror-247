import React from 'react';
import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { Scheduler } from '@jupyterlab/scheduler';
import { pluginIds } from '../constants';
import { CreateNotebookJob } from '../widgets/CreateNotebookJob';
import { PluginEnvironmentProvider, getPluginEnvironment } from '../utils/PluginEnvironmentProvider';

const FEATURE_FLAGS_PLUGIN_ID = "@amzn/sagemaker-ui:featureFlags";
const SCHEDULING_NOTEBOOKS_FEATURE_FLAG = "ScheduleNotebooksReInvent";

export const isSchedulingNotebookFeatureFlag = async (app: JupyterFrontEnd) => {
  let showScheduler = true;
  const pluginEnvironment = getPluginEnvironment(app);
  if (pluginEnvironment.isStudio) {
    const pluginMap: Record<string, any> | undefined = (app as any)._pluginMap;
    if (pluginMap) {
      const featureFlags = await pluginMap[FEATURE_FLAGS_PLUGIN_ID];
      if (!featureFlags) return showScheduler;
      // @ts-ignore -- ignoring as we are waiting on the promise to be resolved before checking if the service exists
      const features = await featureFlags.promise;
      if (featureFlags.service) {
        featureFlags.service.forEach((ff: any) => {
          if (ff.includes(SCHEDULING_NOTEBOOKS_FEATURE_FLAG)) showScheduler = false
        })
      }
    }
  }
  return showScheduler;
}

// This should only load up when the open source @jupyterlab/scheduler extension is installed and activated
// autoStart is set to false as this should only load when a plugin requests the Scheduler.IAdvancedOptions token
const ScheduleNotebookPlugin: JupyterFrontEndPlugin<Scheduler.IAdvancedOptions> = {
  id: pluginIds.SchedulerPlugin,
  autoStart: false,
  requires: [ISettingRegistry],
  provides: Scheduler.IAdvancedOptions,
   activate: async (app: JupyterFrontEnd, settingRegistry: ISettingRegistry) => {
    const showNotebookJob = await isSchedulingNotebookFeatureFlag(app);
    if (!showNotebookJob) {
        document.styleSheets[0].insertRule(
          `li[data-command="scheduling:create-from-filebrowser"] { display: none !important; }`
        );

        document.styleSheets[0].insertRule(`
          button[title="Create notebook job"] { display: none !important; }
        `);

        document.styleSheets[0].insertRule(`
          .jp-create-job-form { display: none !important; }
        `)

        document.styleSheets[0].insertRule(`
          div[title="Notebook Jobs"] { display: none !important; }
        `)
    }
    return (props) => {
      const requestClient = app.serviceManager.serverSettings;
      const contentClient = app.serviceManager.contents;

      if (!showNotebookJob) {
        return null
      };

      return (
        <PluginEnvironmentProvider app={app}>
          <CreateNotebookJob
            requestClient={requestClient}
            contentsManager={contentClient}
            settingRegistry={settingRegistry}
            commands={app.commands}
            {...props}
          />
        </PluginEnvironmentProvider>
      );
    };
  },
};

export { ScheduleNotebookPlugin };

import { resolveSafeChildPath } from '@backstage/backend-plugin-api';
import { createTemplateAction } from '@backstage/plugin-scaffolder-node';
import { z } from 'zod';
import { mkdir, writeFile } from 'node:fs/promises';

export const createCustomAction = () => {
  return createTemplateAction({
    id: 'my:custom:action',
    description: 'Creates a file in the temporary Scaffolder workspace.',
    schema: {
      input: {
        contents: z =>
          z.string({
            description: 'The contents of the file',
          }),
        filename: z =>
          z.string({
            description: 'The filename of the file to create',
          }),
      },
    },
    async handler(ctx) {
      const filePath = resolveSafeChildPath(
        ctx.workspacePath,
        ctx.input.filename,
      );

      await mkdir(ctx.workspacePath, { recursive: true });
      await writeFile(filePath, ctx.input.contents, 'utf8');

      ctx.logger.info(`Created file: ${filePath}`);
    },
  });
};
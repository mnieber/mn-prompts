import React from 'react';
import {
  ModestToolButtonTrim,
  ToolButton,
} from '/src/frames/components/ToolButton';
import { cn } from '/src/utils/classnames';

export type PropsT = {
  tabIndex?: number;
  className?: any;
};

export const usePreviewButton = (props: PropsT) => {
  const [preview, setPreview] = React.useState(false);
  const showPreviewButton = (
    <ToolButton
      className={cn('PreviewButton', props.className)}
      trim={ModestToolButtonTrim}
      iconName={preview ? 'checkFilled' : 'checkEmpty'}
      key="preview"
      label="Preview"
      onClick={() => setPreview(!preview)}
      tabIndex={props.tabIndex ?? 0}
    />
  );

  return {
    preview,
    setPreview,
    showPreviewButton,
  };
};

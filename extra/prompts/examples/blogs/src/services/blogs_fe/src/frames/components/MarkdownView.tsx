import { observer } from 'mobx-react-lite';
import ReactMarkdown from 'react-markdown';
import { withContextProps } from 'react-props-from-context';
import { cn } from '/src/utils/classnames';

// Import styles
import './MarkdownView.scss';

export type PropsT = {
  text: string;
  className?: any;
};

const ContextProps = {};

export const MarkdownView = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    return (
      <div className={cn('MarkdownView', props.className)}>
        <ReactMarkdown>{props.text ?? ''}</ReactMarkdown>
      </div>
    );
  }, ContextProps)
);

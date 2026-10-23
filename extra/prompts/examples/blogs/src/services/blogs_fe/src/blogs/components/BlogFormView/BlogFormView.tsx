import { observer } from 'mobx-react-lite';
import { FormStateProvider } from 'react-form-state-context';
import { withContextProps } from 'react-props-from-context';
import { form } from './form';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import {
  Field,
  FormCancelButton,
  FormFieldLabel,
  FormSaveButton,
  GlobalError,
  MarkdownField,
  NameField,
  SlugField,
} from '/src/forms/components';
import { usePreviewButton } from '/src/forms/hooks/usePreviewButton';
import { CardS } from '/src/frames/components/Card';
import { MainFormS } from '/src/frames/components/MainForm';
import { navStateCtx } from '/src/routes/hooks/useNavStateContext';
import { cn } from '/src/utils/classnames';

// Import styles
import './BlogFormView.scss';

export type PropsT = {
  className?: any;
};

export const ContextProps = {
  navState: navStateCtx.navState,
  blog: blogsCtx.blog,
  blogsEdit: blogsCtx.blogsEdit,
  blogsAddition: blogsCtx.blogsAddition,
};

export const BlogFormView = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const { showPreviewButton, preview } = usePreviewButton({
      tabIndex: 9,
      className: 'font-normal',
    });

    const blog = props.blogsAddition.item || props.blog;
    if (!blog) {
      return null;
    }

    const initialValues = form.getInitialValues(props);
    const initialErrors = form.getInitialErrors(props);

    return (
      //
      // 🔳 BlogFormView 🔳
      //
      <div
        className={cn(CardS.root(), 'BlogFormView', [
          CardS.color.gray(),
          MainFormS.root.padding.default(),
          props.className,
        ])}
      >
        {
          // 🔳 FormStateProvider 🔳
        }
        <FormStateProvider
          initialValues={initialValues}
          initialErrors={initialErrors}
          handleValidate={form.getHandleValidate(props)}
          handleSubmit={form.getHandleSubmit(
            props,
            initialValues,
            initialErrors
          )}
          handleCancel={form.getHandleCancel(props)}
        >
          {
            // 🔳 Global error 🔳
          }
          <GlobalError className={MainFormS.GlobalError()} />
          {
            // 🔳 NameField 🔳
          }
          <Field fieldName="blogForm.name" className={MainFormS.Field()}>
            <FormFieldLabel label="NAME" />
            <NameField
              tabIndex={2}
              controlled={true}
              autoSelect={true}
              slugFieldName={
                initialValues['blogForm.slug'] === '-'
                  ? 'blogForm.slug'
                  : undefined
              }
            />
          </Field>
          {
            // 🔳 SlugField 🔳
          }
          <Field fieldName="blogForm.slug" className={MainFormS.Field()}>
            <FormFieldLabel label="SLUG" />
            <SlugField relatedFieldName="blogForm.name" />
          </Field>
          {
            // 🔳 DescriptionField 🔳
          }
          <Field
            fieldName="blogForm.description"
            tabOnEnter={false}
            className={MainFormS.Field()}
          >
            <FormFieldLabel label="DESCRIPTION" buttons={[showPreviewButton]} />
            <MarkdownField tabIndex={6} controlled={true} preview={preview} />
          </Field>
          {
            // 🔳 Buttons 🔳
          }
          <div className={cn(MainFormS.Buttons())}>
            <FormCancelButton
              theme="MainView"
              className={cn(MainFormS.Button.root(), MainFormS.Button.gap())}
              tabIndex={10}
              label="Cancel"
            />
            <FormSaveButton
              theme="MainView"
              tabIndex={10}
              label="Save"
              className={cn(MainFormS.Button.root())}
            />
          </div>
        </FormStateProvider>
      </div>
    );
  }, ContextProps)
);

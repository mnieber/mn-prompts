import { observer } from 'mobx-react-lite';
import React from 'react';
import { FormStateProvider } from 'react-form-state-context';
import { withContextProps } from 'react-props-from-context';
import { form } from './form';
import { BlogPostT, getBlogPostLevelOptions } from '/src/api/types/BlogPostT';
import { blogPostsCtx } from '/src/blogPosts/hooks/useBlogPostsContext';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import {
  Field,
  FormCancelButton,
  FormFieldLabel,
  FormSaveButton,
  GlobalError,
  MarkdownField,
  NameField,
  ValuePickerField,
} from '/src/forms/components';
import { usePreviewButton } from '/src/forms/hooks/usePreviewButton';
import { CardS } from '/src/frames/components/Card';
import { MainFormS } from '/src/frames/components/MainForm';
import { navStateCtx } from '/src/routes/hooks/useNavStateContext';
import { cn } from '/src/utils/classnames';

// Import styles
import './BlogPostFormView.scss';

export type PropsT = {
  className?: any;
};

export const ContextProps = {
  navState: navStateCtx.navState,
  blog: blogsCtx.blog,
  blogPost: blogPostsCtx.blogPost,
  blogPostsAddition: blogPostsCtx.blogPostsAddition,
  blogPostsEdit: blogPostsCtx.blogPostsEdit,
};

export const BlogPostFormView = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const { showPreviewButton, preview } = usePreviewButton({
      tabIndex: 9,
      className: 'font-normal',
    });

    // The form holds on to the blog post that it opened with. It stays open when the blog
    // post leaves the list (because someone else deleted it), and a refetch doesn't reset
    // what the user typed.
    const blogPostRef = React.useRef<BlogPostT>();
    blogPostRef.current ??= props.blogPostsAddition.item ?? props.blogPost;
    const blogPost = blogPostRef.current;
    if (!blogPost) {
      return null;
    }

    const initialValues = form.getInitialValues(blogPost);
    const initialErrors = form.getInitialErrors(props);

    return (
      //
      // 🔳 BlogPostFormView 🔳
      //
      <div
        className={cn(CardS.root(), 'BlogPostFormView', [
          CardS.color.surface(),
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
            // 🔳 TitleField 🔳
          }
          <Field fieldName="blogPostForm.title" className={MainFormS.Field()}>
            <FormFieldLabel label="TITLE" />
            <NameField tabIndex={2} controlled={true} autoSelect={true} />
          </Field>
          {
            // 🔳 ContentField 🔳
          }
          <Field
            fieldName="blogPostForm.content"
            tabOnEnter={false}
            className={MainFormS.Field()}
          >
            <FormFieldLabel label="CONTENT" buttons={[showPreviewButton]} />
            <MarkdownField tabIndex={6} controlled={true} preview={preview} />
          </Field>
          {
            // 🔳 LevelField 🔳
          }
          <Field
            fieldName="blogPostForm.level"
            tabOnEnter={false}
            className={MainFormS.Field()}
          >
            <FormFieldLabel label="LEVEL" />
            <ValuePickerField
              tabIndex={7}
              isCreatable={false}
              isMulti={false}
              tabOnEnter={false}
              labelFromValue={(x: any) => x}
              loadOptions={getBlogPostLevelOptions}
              defaultOptions
            />
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

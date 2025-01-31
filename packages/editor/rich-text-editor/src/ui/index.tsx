"use client";
import * as React from "react";
import {
  EditorContainer,
  EditorContentWrapper,
  getEditorClassNames,
  useEditor,
} from "@plane/editor-core";
import { EditorBubbleMenu } from "./menus/bubble-menu";
import { RichTextEditorExtensions } from "./extensions";

export type UploadImage = (file: File) => Promise<string>;
export type DeleteImage = (assetUrlWithWorkspaceId: string) => Promise<any>;
export type ValidateImage = (assetUrlWithWorkspaceId: string) => Promise<any>;

export type IMentionSuggestion = {
  id: string;
  type: string;
  avatar: string;
  title: string;
  subtitle: string;
  redirect_uri: string;
};

export type IMentionHighlight = string;

interface IRichTextEditor {
  value: string;
  dragDropEnabled?: boolean;
  uploadFile: UploadImage;
  deleteFile: DeleteImage;
  validateFile?: ValidateImage;
  noBorder?: boolean;
  borderOnFocus?: boolean;
  cancelUploadImage?: () => any;
  customClassName?: string;
  editorContentCustomClassNames?: string;
  onChange?: (json: any, html: string) => void;
  setIsSubmitting?: (
    isSubmitting: "submitting" | "submitted" | "saved",
  ) => void;
  setShouldShowAlert?: (showAlert: boolean) => void;
  forwardedRef?: any;
  debouncedUpdatesEnabled?: boolean;
  mentionHighlights?: string[];
  mentionSuggestions?: IMentionSuggestion[];
}

interface RichTextEditorProps extends IRichTextEditor {
  forwardedRef?: React.Ref<EditorHandle>;
}

interface EditorHandle {
  clearEditor: () => void;
  setEditorValue: (content: string) => void;
}

const RichTextEditor = ({
  onChange,
  dragDropEnabled,
  debouncedUpdatesEnabled,
  setIsSubmitting,
  setShouldShowAlert,
  editorContentCustomClassNames,
  value,
  uploadFile,
  deleteFile,
  validateFile,
  noBorder,
  cancelUploadImage,
  borderOnFocus,
  customClassName,
  forwardedRef,
  mentionHighlights,
  mentionSuggestions,
}: RichTextEditorProps) => {
  const editor = useEditor({
    onChange,
    debouncedUpdatesEnabled,
    setIsSubmitting,
    setShouldShowAlert,
    value,
    uploadFile,
    cancelUploadImage,
    validateFile,
    deleteFile,
    forwardedRef,
    extensions: RichTextEditorExtensions(
      uploadFile,
      setIsSubmitting,
      dragDropEnabled,
    ),
    mentionHighlights,
    mentionSuggestions,
  });

  const editorClassNames = getEditorClassNames({
    noBorder,
    borderOnFocus,
    customClassName,
  });

  if (!editor) return null;

  return (
    <EditorContainer editor={editor} editorClassNames={editorClassNames}>
      {editor && <EditorBubbleMenu editor={editor} />}
      <div className="flex flex-col">
        <EditorContentWrapper
          editor={editor}
          editorContentCustomClassNames={editorContentCustomClassNames}
        />
      </div>
    </EditorContainer>
  );
};

const RichTextEditorWithRef = React.forwardRef<EditorHandle, IRichTextEditor>(
  (props, ref) => <RichTextEditor {...props} forwardedRef={ref} />,
);

RichTextEditorWithRef.displayName = "RichTextEditorWithRef";

export { RichTextEditor, RichTextEditorWithRef };

/** The rule of the real backend for the text in a form. */
export const hasForbiddenWords = (text: string | null | undefined) => {
  return !!text && text.toLowerCase().includes('forbidden');
};

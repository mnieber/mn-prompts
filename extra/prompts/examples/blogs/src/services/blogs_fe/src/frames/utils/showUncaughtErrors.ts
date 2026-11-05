import { getFailureMessage } from '/src/api/utils/getFailureMessage';
import { errorBannerState } from '/src/frames/errorBannerState';

// Shows the errors that no code handled in the ErrorBanner. These are bugs, since a
// failed request is a result. Don't call preventDefault here: the errors must still
// reach the console, and fail the tests.
export const showUncaughtErrors = () => {
  window.addEventListener('unhandledrejection', (event) => {
    errorBannerState.show(getFailureMessage(event.reason));
  });

  window.addEventListener('error', (event) => {
    // Browser notices (e.g. "ResizeObserver loop completed") have no error object
    if (event.error) {
      errorBannerState.show(getFailureMessage(event.error));
    }
  });
};

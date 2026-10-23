import React from 'react';

export function useScheduledCall(callback: Function) {
  const [scheduled, setScheduled] = React.useState<boolean>(false);

  React.useEffect(() => {
    if (scheduled) {
      setScheduled(false);
      callback();
    }
  }, [scheduled, callback]);

  return () => setScheduled(true);
}

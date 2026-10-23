import { MockDashboardFrame } from '/src/mocks/frames/components/MockDashboardFrame';
import { MockMainView } from '/src/mocks/frames/components/MockMainView';

export const MockApp = () => {
  return (
    <MockDashboardFrame>
      <MockMainView className=""></MockMainView>
    </MockDashboardFrame>
  );
};

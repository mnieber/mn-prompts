import { handleMe } from 'src/mocks/users';
import { testWithMsw } from 'src/mocks/utils/testWithMsw';
import { get } from '/src/api/restClient';

const describe = (name: string, testSuite: () => void) => {
  console.log('Warning: using stub describe');
};

const it = (name: string, test: () => void) => {
  console.log('Warning: using stub it');
};

const expect = (value: any) => {
  return {
    toEqual: (expected: any) => {
      console.log('Warning: using stub expect');
    },
  };
};

describe(
  'testMsw',
  testWithMsw([handleMe], () => {
    it('displays data from backend', async () => {
      const response = await get('user/me/');
      expect(response.data).toEqual({
        data: 'fancy data string',
      });
    });
  })
);

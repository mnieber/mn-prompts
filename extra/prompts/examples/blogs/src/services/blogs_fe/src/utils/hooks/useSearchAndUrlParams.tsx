import * as R from 'ramda';
import { mergeLeft } from 'ramda';
import { useParams } from 'wouter';
import { history } from '/src/routes/history';
import { ObjT } from '/src/utils/types';

export const useSearchAndUrlParams = (): ObjT => {
  const params = useParams();
  const searchParams = new URLSearchParams(history.location.search);
  const searchParamMap = R.fromPairs(Array.from(searchParams.entries()));
  return mergeLeft(params, searchParamMap);
};

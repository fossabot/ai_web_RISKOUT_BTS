import { atom } from 'recoil';

/* Component 에서 필요로 하는 데이터 형식
{
  contentsLength: 0,
  contents: [],
  filterTags: {
    ORG: {},
    CVL: {},
    TIM: {},
}
*/

const initialState = {
  contentsLength: 0,
  contents: [],
  filterTags: {
    ORG: {},
    CVL: {},
    TIM: {},
  },
};

export const searchListState = atom({
  key: 'searchListState',
  default: initialState,
});

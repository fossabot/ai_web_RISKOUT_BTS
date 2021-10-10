import { atom } from 'recoil';

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

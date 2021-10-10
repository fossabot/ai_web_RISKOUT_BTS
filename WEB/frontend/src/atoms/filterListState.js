import { atom } from 'recoil';

// 배포시 삭제
const initialState = ['GP/GOP', '정체단', '사이버작전센터'];

export const filterListState = atom({
  key: 'filterListState',
  default: initialState,
});

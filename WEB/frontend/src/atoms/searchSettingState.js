import { atom, selector } from 'recoil';
import { filterListState } from './filterListState';

// 검색할 때 넘기는 DateRange와 Filter 를 정의하는 atom
export const searchSettingState = selector({
  key: 'searchSettingState',
  get: ({ get }) => {
    const filter = get(filterListState);
    const dateRange = 24; // 시간 단위(init은 24시간)
    return { filter: filter, dateRange: dateRange };
  },
});

export const dateRangeState = selector({
  key: 'dateRangeState',
  get: ({ get }) => get(searchSettingState).dateRange,
  set: ({ set }, newValue) => {
    set(searchSettingState, newValue);
  },
});

import { atom, selector } from 'recoil';
import { filterListState } from './filterListState';

// 검색할 때 넘기는 DateRange와 Filter 를 정의하는 atom
export const searchSettingState = selector({
  key: 'searchSettingState',
  get: ({ get }) => {
    const filter = get(filterListState);
    const dateRange = {
      startDate: {
        year: 1985,
        month: 1,
      },
      endDate: (() => {
        const d = new Date();
        return {
          year: d.getFullYear(),
          month: d.getMonth() + 1,
        };
      })(),
    };
    return { filter: filter, dateRange: dateRange };
  },
});

export const dateRangeState = selector({
  key: 'dateRangeState',
  get: ({ get }) => {
    const searchSetting = get(searchSettingState);
    return searchSetting.dateRange;
  },
});

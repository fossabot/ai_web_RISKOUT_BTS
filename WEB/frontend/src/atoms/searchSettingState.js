import { atom } from 'recoil';

const initialState = {
  dateRange: {
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
  },
};

// 검색할 때 넘기는 DateRange와 Filter 를 정의하는 atom
export const searchSettingState = atom({
  key: 'searchSettingState',
  default: initialState,
});

export const dateRangeState = selector({
  key: 'dateRangeState',
  get: ({ get }) => {
    const searchSetting = get(searchSettingState);
    return searchSetting.dateRange;
  },
});

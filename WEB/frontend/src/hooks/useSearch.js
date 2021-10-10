import { useEffect } from 'react';
import axios from 'axios';

import { useRecoilState, useRecoilValue } from 'recoil';
import { searchListState } from '../atoms/searchListState';
import { filterListState } from '../atoms/filterListState';

export default function useSeacrh() {
  const [searchList, setSearchList] = useRecoilState(searchListState);
  const filterList = useRecoilValue(filterListState);
  useEffect(() => {
    //TODO: API 서버 배포시 수정
    const searchUrl = `/static/SecretData.example.json`;
    async function fetchSearch() {
      axios.get(searchUrl).then((data) => {
        setSearchList(data.data);
        console.log(data.data);
      });
    }

    fetchSearch();
  }, [filterList]);
}

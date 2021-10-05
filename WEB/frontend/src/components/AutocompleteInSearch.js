import React, {useState} from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';

export default function AutocompleteInSearch(onChange){
 
  return(    
    <Autocomplete
      onChange={onChange}
      multiple
      freeSolo
      id="tags-outlined"
      options={people}
      sx={{ width: '100%'}}
      getOptionLabel={(option) => option.name}
      //defaultValue={} 첫 렌더링 시 기본으로 설정될 필터
      renderInput={(params) => <TextField {...params} type="input" variant="outlined" margin="dense"/>}
    / >
  );
};

const people = [
  {
    name: '이원빈',
    age: '22',
  },
  {
    name: '서종찬',
    age: '22',
  },
  {
    name: '서명근',
    age: '22',
  },
  {
    name: '김태원',
    age: '20',
  },
  {
    name: '이민식',
    age: '25',
  },
  {
    name: '박용준',
    age: '20',
  },
  {
    name: '조정환',
    age: '23',
  },
  {
    name: '김선균',
    age: '22',
  },
  {
    name: '오정도',
    age: '22',
  },
  {
    name: '최원용',
    age: '22',
  },
  {
    name: '김태완',
    age: '20',
  },
  {
    name: '박도범',
    age: '25',
  },
  {
    name: '손의섭',
    age: '20',
  },
  {
    name: '손정호',
    age: '23',
  },
  {
    name: '오희호',
    age: '23',
  },
  {
    name: '문자석',
    age: '22',
  },
  {
    name: '홍길동',
    age: '22',
  },
  {
    name: '신해진',
    age: '22',
  },
  {
    name: '한정진',
    age: '20',
  },
  {
    name: '이정빈',
    age: '25',
  },
  {
    name: '손길동',
    age: '20',
  },
  {
    name: '윤세준',
    age: '23',
  },
];


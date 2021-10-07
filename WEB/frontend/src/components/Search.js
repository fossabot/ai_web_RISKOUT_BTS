import React, {useState} from 'react';
import Box from '@mui/material/Box';
import AutocompleteInSearch from './AutocompleteInSearch';
import Button from '@mui/material/Button';
import SearchIcon from '@mui/icons-material/Search';
import {sampleData, sampleOptions} from './sample.js';
// import "../App.css";


export default function Search() {
  const onSubmit = (e) => {
    const textValue = e.target.value;
    console.log(textValue);
  };
  
  return (
    <Box>
      <form onSubmit={onSubmit} style={{display: 'flex'}}>
        <AutocompleteInSearch />
        <Button
          sx={{ width: "", height: '5.1em' }}
          variant="contained"
          type="submit"
        ><SearchIcon /></Button>
      </form>
    </Box>
  );
}



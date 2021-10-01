import React from 'react';
import Box from "@mui/material/Box";
import Search from '../components/Search';
import '../css/Header.css';

const Secret = () => {
    return (
        <Box>
        <section id="sub_contents">
		<div class="sub01_wrap">
          <Search />
		</div>
	</section>
    </Box>
    );
};

export default Secret;
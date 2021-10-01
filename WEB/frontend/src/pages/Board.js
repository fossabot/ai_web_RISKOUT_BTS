import React from 'react';
import Box from "@mui/material/Box";
import '../css/Header.css';
import Search from '../components/Search';

const Board = () => {
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

export default Board;
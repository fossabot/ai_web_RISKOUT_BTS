import React, { useState, useEffect } from 'react';
import { Route } from 'react-router-dom';
import '../App.css';
import icon01 from '../images/sub/btn_icon01.png';
import icon02 from '../images/sub/btn_icon02.png';
import icon03 from '../images/sub/btn_icon03.png';
import Layout from '../layout';
import Sidebar from '../components/Sidebar';

function App() {

	return (
		<Layout>
			<Sidebar />
			
		</Layout>
	);
}

export default App;
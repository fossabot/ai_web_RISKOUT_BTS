import React from 'react';

import Helmet from 'react-helmet';
// import '../css//normalize.css';
import '../css/style_tab.css';
import '../css/style_mob.css';
import '../css/slick.css';
import '../css/jquery.fullpage.css';
import '../css/style.css';

// MUI Styles
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import SideNavigation from '../components/Modal/SideNavigation';




const drawerWidth = 240;

const Main = styled("main", { shouldForwardProp: (prop) => prop !== "open" })(
  ({ theme, open }) => ({
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create("margin", {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen
    }),
    marginLeft: `-${drawerWidth}px`,
    ...(open && {
      transition: theme.transitions.create("margin", {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen
      }),
      marginLeft: 0
    })
  })
);

export default class MainLayout extends React.Component {
  render() {
    const { children, handleLogout, open } = this.props;
    return (
      // Helmet에 문제가 있는 것 같아 잠시 주석처리
      // cf. https://stackoverflow.com/questions/62202890/how-can-i-fix-using-unsafe-componentwillmount-in-strict-mode-is-not-recommended#comment118614308_62202890
      // <Helmet>
      //   <meta name="description" content="my-layout" />
      // </Helmet> 

      <Box display="flex">
        <Box>
          <Box sx={{ display: "flex" }}>
            <SideNavigation handleLogout={handleLogout} >
            </SideNavigation>

            <Main open={open}>

              {children}
            </Main>


          </Box>
        </Box>
      </Box>
    );
  }
}

import React from 'react';
import Helmet from 'react-helmet';
// import '../css//normalize.css';
import '../css/style_tab.css';
import '../css/style_mob.css';
import '../css/slick.css';
import '../css/jquery.fullpage.css';
import '../css/style.css';

export default class MainLayout extends React.Component {
  render() {
    const { children } = this.props;
    return (
      <div>
        {/* 
        // Helmet에 문제가 있는 것 같아 잠시 주석처리
        // cf. https://stackoverflow.com/questions/62202890/how-can-i-fix-using-unsafe-componentwillmount-in-strict-mode-is-not-recommended#comment118614308_62202890
        <Helmet>
          <meta name="description" content="my-layout" />
        </Helmet> 
        */}
        {children}
      </div>
    );
  }
}

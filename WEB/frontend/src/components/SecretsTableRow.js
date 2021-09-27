import React from 'react';
import fileIcon from '../images/sub/file.png';

export default function tableRow(props) {
    const { title, preview, author, href } = props;
    const showDetailModal = () => {
        console.log('TODO: show modal for ', title);
    }
    return (
        <tr>
            <td><a href={href} title="외부링크"><img src={fileIcon} alt="filetype" /></a></td>
            <td onClick={showDetailModal} style={{cursor: "pointer"}}>
                <h3>{title}</h3>
                <p>{preview}</p>
            </td>
            <td>{author}</td>
        </tr>

    )

}


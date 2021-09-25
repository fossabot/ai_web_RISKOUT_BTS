import React from 'react';
import fileIcon from '../images/sub/file.png';

export default function tableRow(props) {
    const { title, preview, author } = props;
    return (
        <tr>
            <td><img src={fileIcon} alt="" /></td>
            <td>
                <h3>{title}</h3>
                <p>{preview}</p>
            </td>
            <td>{author}</td>
        </tr>

    )

}


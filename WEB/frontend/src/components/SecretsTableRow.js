import React from 'react';

export default function tableRow(props) {
    const { title, preview, author } = props;
    return (
        <tr>
            <td><img src="images/sub/file.png" alt="" /></td>
            <td>
                <h3>{title}</h3>
                <p>{preview}</p>
            </td>
            <td>{author}</td>
        </tr>

    )

}
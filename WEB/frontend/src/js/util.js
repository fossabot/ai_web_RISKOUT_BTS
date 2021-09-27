/**
 * Split on highlight term and include term into parts, ignore case
 * Code snippet from https://stackoverflow.com/a/43235785
 * @param {*} text 
 * @param {*} highlight 
 * @returns requested parts are highlighted with <b>
 */
function getHighlightedText(text, highlight) {
    const parts = text.split(new RegExp(`(${highlight})`, 'gi'));
    return (
        <span> {parts.map((part, i) =>
            <span key={i} style={part.toLowerCase() === highlight.toLowerCase() ? { fontWeight: 'bold' } : {}}>
                {part}
            </span>)
        } </span>
    );
}

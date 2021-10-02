import ReactDOMServer from "react-dom/server";

/**
 * Split on highlight term and include term into parts, ignore case
 * Code snippet adapted from https://stackoverflow.com/a/43235785
 * @param {*} text
 * @param {*} highlight
 * @returns requested parts are highlighted with <b>
 */
function getHighlightedText(text, highlight) {
  const parts = text.split(new RegExp(`(${highlight})`, "gi"));
  return (
    <span>
      {" "}
      {parts.map((part, i) =>
        part.toLowerCase() === highlight.toLowerCase() ? (
          <mark key={i}>{part}</mark>
        ) : (
          <span key={i}>{part}</span>
        )
      )}{" "}
    </span>
  );
}

function getLineBreakText(text) {
  console.log("getlinebreak", text, ReactDOMServer.renderToString(text));
  return ReactDOMServer.renderToString(text)
    .split("\n")
    .map((str) => <p>{str}</p>);
}

/**
 * Get text content of JSX element
 * Code snippet from https://stackoverflow.com/a/60564620
 * @param {*} node JSX element node
 * @returns String of the text content
 */
function getNodeText(node) {
  if (["string", "number"].includes(typeof node)) return node;
  if (node instanceof Array) return node.map(getNodeText).join("");
  if (typeof node === "object" && node) return getNodeText(node.props.children);
}

function decodeNewline(text, multiplier) {
  return text.replace(/\\n/g, "\n".repeat(multiplier));
}

export {
  getHighlightedText,
  getLineBreakText,
  getNodeText,
  decodeNewline as replaceNewline,
};

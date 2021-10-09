// shapeData
export function shapeData(data, headers) {
    const bounds = headers ? headers.length : boundsFromRowData(data.rows);
  
    const shapedRowData = data.rows.map((row, index) => {
      let mRow = row.slice(0, bounds);
      // adds empty cells if no headers and bounds are greater than the row lengths
      if (row.length < bounds) {
        for (let i = 0; i < bounds - row.length; i++) {
          mRow.push("");
        }
      }
      return mRow;
    });
  
    let shapedHeaders;
    if (headers) shapedHeaders = headers;
    else {
      let hdrArr = [];
      for (let i = 0; i < bounds; i++) {
        hdrArr.push(i + 1);
      }
      shapedHeaders = hdrArr;
    }
  
    return {
      headers: shapedHeaders,
      rows: shapedRowData,
      bounds
    };
  }
  
  // gets the max length (column count) of all rows via reducer
  const boundsFromRowData = (rows) =>
    rows.map((r) => r.length).reduce((acc, cv) => (cv > acc ? cv : acc));
  
  // basic sorting method
  export function sort(data, { colIndex, direction }) {
    return data.sort((a, b) => {
      const r = /[A-Za-z]/;
      if (direction === "desc") {
        return (
          r.test(b[colIndex]) - r.test(a[colIndex]) ||
          (a[colIndex] > b[colIndex] ? -1 : a[colIndex] < b[colIndex] ? 1 : 0)
        );
      } else {
        return (
          r.test(a[colIndex]) - r.test(b[colIndex]) ||
          (a[colIndex] < b[colIndex] ? -1 : a[colIndex] > b[colIndex] ? 1 : 0)
        );
      }
    });
  }
  
  // search 함수
  export function search(data, query) {
    return {
      ...data,
      rows: data.rows.filter((d) => {
        let match = false;
        d.forEach((n) => {
          if (n.toString().includes(query)) {
            match = true;
          }
        });
        return match;
      })
    };
  }
  
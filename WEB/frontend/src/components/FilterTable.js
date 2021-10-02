import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import "../App.css";

function createData(type, subject, writer) {
  return { type, subject, writer };
}

// 테이블 내 들어갈 필터링 후 검색될 내용을 담는 변수
const rows = [
  createData("Frozen yoghurt", "해군 참모총장 만난 썰 푼다", "이민식"),
  createData("Ice cream sandwich", "오진석 소위 임관 실화냐..", "김태완"),
  createData("Eclair", "2함대 출항시간 뭐냐..", "이정빈"),
  createData("Cupcake", "갑자기 태풍와서 피항간 썰 푼다", "오정도"),
  createData("Gingerbread", "3함대 젓가락 살인마 썰푼다", "문자석"),

  createData("Jam", "계룡에서 박보검 본 썰푼다", "손정호"),
  createData("Cookie", "Cert업무 강도 에바참치임..", "서명곤"),
  createData("Eclair", "2함대 출항시간 뭐냐..", "이정빈"),
  createData("Cupcake", "갑자기 태풍와서 피항간 썰 푼다", "오정도"),
  createData("Gingerbread", "3함대 젓가락 살인마 썰푼다", "문자석"),
  createData("Jam", "계룡에서 박보검 본 썰푼다", "손정호"),
  createData("Cookie", "Cert업무 강도 에바참치임..", "서명곤"),
  createData("Eclair", "2함대 출항시간 뭐냐..", "이정빈"),
  createData("Cupcake", "갑자기 태풍와서 피항간 썰 푼다", "오정도"),
  createData("Gingerbread", "3함대 젓가락 살인마 썰푼다", "문자석"),
  createData("Jam", "계룡에서 박보검 본 썰푼다", "손정호"),
  createData("Cookie", "Cert업무 강도 에바참치임..", "서명곤"),
  createData("Eclair", "2함대 출항시간 뭐냐..", "이정빈"),
  createData("Cupcake", "갑자기 태풍와서 피항간 썰 푼다", "오정도"),
  createData("Gingerbread", "3함대 젓가락 살인마 썰푼다", "문자석"),
  createData("Jam", "계룡에서 박보검 본 썰푼다", "손정호"),
  createData("Cookie", "Cert업무 강도 에바참치임..", "서명곤"),
  createData("Eclair", "2함대 출항시간 뭐냐..", "이정빈"),
  createData("Cupcake", "갑자기 태풍와서 피항간 썰 푼다", "오정도"),
  createData("Gingerbread", "3함대 젓가락 살인마 썰푼다", "문자석"),
  createData("Jam", "계룡에서 박보검 본 썰푼다", "손정호"),
  createData("Cookie", "Cert업무 강도 에바참치임..", "서명곤")
];

export default function filterTable() {
  return (
    <TableContainer>
      <Table sx={{ minWidth: 500 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell align="center">유형&nbsp;(type)</TableCell>
            <TableCell align="center">제목&nbsp;(title)</TableCell>
            <TableCell align="center">글쓴이&nbsp;(writer)</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.type}
              sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
            >
              <TableCell align="center" component="th" scope="row">
                {row.type}
              </TableCell>
              <TableCell align="center">{row.subject}</TableCell>
              <TableCell align="center">{row.writer}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

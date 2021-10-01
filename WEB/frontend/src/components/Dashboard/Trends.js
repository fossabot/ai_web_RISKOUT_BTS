import {
  Card,
  CardHeader,
  CardContent,
  Box,
  Button,
  Divider,
  LinearProgress,
} from '@mui/material';
import { DataGrid, GridRowsProp, GridColDef } from '@mui/x-data-grid';

const rows = [
  {
    id: 1,
    title: '9월 수출 558억 달러, 65년 무역 역사상 최고치…두 달 만에 기록 경신',
    date: new Date('2021-10-01'),
  },
  {
    id: 2,
    title: '“억지 부리지 말라”…野주자들, 이준석 때린 조수진 질타',
    date: new Date('2021-5-05'),
  },
  {
    id: 3,
    title: '급성 복통으로 출석 미룬 유동규…검찰, 응급실서 체포',
    date: new Date('2021-11-15'),
  },
];

const columns = [
  {
    field: 'trueScore',
    headerName: '가짜뉴스',
    widght: 100,
    renderCell: (params) => <div>{Number(params.value)}</div>,
  },
  { field: 'title', headerName: '제목', flex: 1, minWidth: 150 },
  {
    field: 'date',
    headerName: '날짜',
    width: 100,
    renderCell: (params) => (
      <strong>{params.value.toLocaleDateString()}</strong>
    ),
  },
  { field: 'keywords', headerName: '키워드', width: 150 },
];

export default function Trends({ articles }) {
  return (
    <Card style={{ height: '400px' }}>
      <CardHeader title="트렌드" />
      <Divider />
      <CardContent>
        <Box sx={{ height: 300, width: '100%' }}>
          <DataGrid rows={rows} columns={columns} />
        </Box>
      </CardContent>
    </Card>
  );
}

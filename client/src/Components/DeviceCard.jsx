import { Card, CardMedia, Box,CardContent, Typography, Container } from "@mui/material";
import { React, useEffect ,useState} from "react";

function DeviceCard({ label ,graph,graph2 }) {
  const [clicked,setClicked] = useState("None")

  const handleClick = () => 
  {
    
    if (clicked == "None")
    {
      setClicked("box")
    }
    if (clicked == "box")
    {
      setClicked("None")
    }
  }
  return (
    <div
    style={{
        display: "flex",
        width : "60%",
        alignItems:"center",
        justifyContent:"center",
      }}
    >
      <Card
        
        className="property-card"
        style={{
          display: "flex",
          margin: "20px",
          width : "90%",
          alignItems:"center",
          justifyContent:"center",
          padding:"20px",
          boxShadow: "0 2px 10px rgba(0, 0, 0, 0.1)",
          
        }}
      >
        <Box style={{ display: "flex", flexDirection: "column", flex: 1 }}>
          <CardContent
            style={{
              display: "flex",
              flexDirection: "column",
              flex: 1,
              alignItems:"center",
              justifyContent:"center",
              padding: "20px",
              backgroundColor: "#ffffff",
              color: "#000000",
            }}
          >
            <Typography
                onClick={()=>handleClick()}

            sx = {{ cursor : "pointer",fontSize : "large",margin:"10px",fontWeight:"bold"}}>
              {label}
            </Typography>
            <Container sx = {{ maxWidth:"100%" , display : clicked}} >

            <Container sx = {{  maxWidth:"100% !Important",margin:"10px"}}>

            {graph}
            </Container>
            <Container sx = {{ maxWidth:"100% !Important",margin:"10px"}}>

            {graph2}
            </Container>
            </Container>

          </CardContent>
        </Box>
      </Card>
    </div>
  );
}

export default DeviceCard;

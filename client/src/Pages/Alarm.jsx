import { React, useEffect, useState } from "react";
import DeviceCard from "../Components/DeviceCard";

function Alarm() {
  const [fromTimestamp, setFromTimestamp] = useState(0);
  const [toTimestamp, setToTimestamp] = useState(0);

  useEffect(() => {
    const now = new Date();
    const oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000); // Subtract 1 hour in milliseconds

    setFromTimestamp(oneHourAgo.getTime());
    setToTimestamp(now.getTime());
  }, []);

  return (
    <div
      style={{
        display: "flex",
        width: "100%",
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column",
        marginTop : "100px"

      }}
    >
      <DeviceCard
        label={"Alarm"}
        graph={
          <iframe
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=29`}
            width="100%"
            height="1000"
            frameborder="0"
          ></iframe>
        }
      />
    </div>
  );
}

export default Alarm;

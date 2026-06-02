import React from "react";
import { Composition } from "remotion";
import { Fitshark } from "./Fitshark";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Fitshark"
    component={Fitshark}
    durationInFrames={3600}
    fps={30}
    width={1920}
    height={1080}
  />
);

import { loadFont as loadPoppins } from "@remotion/google-fonts/Poppins";
import { loadFont as loadLora } from "@remotion/google-fonts/Lora";

export const { fontFamily: HEAD } = loadPoppins("normal", {
  weights: ["400", "500", "600", "700"],
});
export const { fontFamily: BODY } = loadLora("normal", { weights: ["400", "500"] });

// Anthropic brand palette
export const C = {
  cream: "#faf9f5",
  dark: "#141413",
  gray: "#b0aea5",
  lightGray: "#e8e6dc",
  clay: "#d97757",
  blue: "#6a9bcc",
  green: "#788c5d",
};

export const FPS = 30;

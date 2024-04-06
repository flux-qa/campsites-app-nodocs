import React from "react";
import { ThemeIcon, Tooltip } from "@mantine/core";
import { Icon } from "@iconify/react";

type AmenityIconProps = {
  icon: string;
  status: boolean | null; // null being unknown
  description?: string;
  size: "md" | "lg";
};

const AmenityIcon = (props: AmenityIconProps) => {
  const color =
    props.status !== null ? (props.status ? "green" : "red") : "gray";

  const variant =
    props.status !== null ? (props.status ? "filled" : "outline") : "light";

  const pixelSize = {
    md: 16,
    lg: 24,
  }[props.size];

  return (
    <Tooltip
      multiline
      position="top-start"
      width={200}
      label={props.description}
      disabled={!props.description}
    >
      <ThemeIcon radius="xl" size={props.size} variant={variant} color={color}>
        <Icon icon={props.icon} width={pixelSize} height={pixelSize} />
      </ThemeIcon>
    </Tooltip>
  );
};

export default AmenityIcon;

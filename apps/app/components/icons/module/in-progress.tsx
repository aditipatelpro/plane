import React from "react";

type Props = {
  width?: string;
  height?: string;
  className?: string;
  color?: string;
};

export const ModuleInProgressIcon: React.FC<Props> = ({
  width = "20",
  height = "20",
  className,
}) => (
  <svg
    width={width}
    height={height}
    className={className}
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 234.83 234.82"
  >
    <g id="Layer_2" data-name="Layer 2">
      <g id="Layer_1-2" data-name="Layer 1">
        <path fill="#f7b964" d="M0,111.14c.63.7.21,1.53.3,2.29-.07.26-.17.28-.3,0Z" />
        <path fill="#f6ab3e" d="M0,119.46a3.11,3.11,0,0,1,.3,2q-.19.33-.3,0Z" />
        <path
          fill="#facf96"
          d="M.27,123.16c0,.66.38,1.38-.27,2v-2C.13,122.89.22,122.91.27,123.16Z"
        />
        <path fill="#f5a939" d="M0,113.47l.3,0a2.39,2.39,0,0,1-.3,1.71Z" />
        <path fill="#f8ba67" d="M.27,123.16a.63.63,0,0,1-.27,0v-1.66l.3,0Z" />
        <path
          fill="#f39e1f"
          d="M234.58,106.92a72,72,0,0,0-.65-8.42,117.08,117.08,0,0,0-13.46-38.74,118.87,118.87,0,0,0-31.73-36.49A115,115,0,0,0,151.17,4.14,83.24,83.24,0,0,0,134.28.58c-2.94-.24-5.89-.22-8.83-.58h-4a2.66,2.66,0,0,1-2,0h-4.32a3.45,3.45,0,0,1-2.33,0h-3.66c-.51.33-1.08.14-1.62.16A87.24,87.24,0,0,0,90,2.35,118.53,118.53,0,0,0,23.16,46,115.24,115.24,0,0,0,4.29,83,85.41,85.41,0,0,0,.6,100.15c-.26,3-.22,6-.6,9v2a6.63,6.63,0,0,1,.17,2.26c-.08.58.17,1.19-.17,1.74v4.32c.35.66.08,1.37.17,2.05v1.57c-.09.68.18,1.39-.17,2v.67c.3.39.14.85.16,1.28.2,3.18.22,6.38.66,9.53a101.21,101.21,0,0,0,4.27,17.76A118.17,118.17,0,0,0,99,234a100.25,100.25,0,0,0,11.37.65,167.86,167.86,0,0,0,23.84-.54,100.39,100.39,0,0,0,23.35-5.72,117.87,117.87,0,0,0,39.67-24.08,117.77,117.77,0,0,0,33.27-53.2,85.63,85.63,0,0,0,3.71-17.37A212.22,212.22,0,0,0,234.58,106.92ZM117.31,217a99.63,99.63,0,0,1-99.7-100.05c0-54.91,44.8-99.35,100.09-99.33,54.89,0,99.32,44.83,99.29,100.14C217,172.43,172.21,217,117.31,217Z"
        />
        <path
          fill="#f39e1f"
          d="M117.33,44a84.49,84.49,0,0,1,12.9,1.15c1.09.19,1.37.56,1.15,1.6q-1.51,7.41-2.94,14.82c-.16.82-.45,1.11-1.33.95a53.31,53.31,0,0,0-19.67,0c-.77.14-1.11-.06-1.26-.83q-1.47-7.59-3-15.16c-.2-1,.21-1.19,1.08-1.35A80.7,80.7,0,0,1,117.33,44Z"
        />
        <path
          fill="#f39e1f"
          d="M44,117.2a80.88,80.88,0,0,1,1.17-12.9c.18-1,.49-1.3,1.49-1.1q7.49,1.53,15,3c.89.18,1,.59.85,1.39a53.54,53.54,0,0,0,0,19.51c.15.83,0,1.2-.88,1.36-5,1-10,2-15,3-.85.17-1.25,0-1.43-1A82.68,82.68,0,0,1,44,117.2Z"
        />
        <path
          fill="#f39e1f"
          d="M190.64,117.39a80.88,80.88,0,0,1-1.17,12.9c-.18,1-.46,1.32-1.48,1.11q-7.49-1.53-15-3c-.88-.17-1-.57-.86-1.38a53.54,53.54,0,0,0,0-19.51c-.18-1,.16-1.23,1-1.39q7.33-1.41,14.66-2.91c1-.21,1.46-.09,1.65,1.08A86.71,86.71,0,0,1,190.64,117.39Z"
        />
        <path
          fill="#f39e1f"
          d="M117.28,190.64a83.24,83.24,0,0,1-12.9-1.15c-1.07-.19-1.38-.53-1.16-1.6q1.52-7.39,2.94-14.82c.16-.8.43-1.12,1.32-.95a53.31,53.31,0,0,0,19.67,0c.92-.17,1.14.2,1.29,1q1.44,7.42,2.95,14.82c.19.95,0,1.35-1,1.54A83,83,0,0,1,117.28,190.64Z"
        />
        <path
          fill="#f39e1f"
          d="M70.7,86.15,70,85.74c-4.23-2.84-8.45-5.69-12.71-8.49-.76-.5-.93-.86-.36-1.67A75.59,75.59,0,0,1,75.41,57.11c.85-.6,1.29-.66,1.93.33,2.71,4.18,5.5,8.3,8.3,12.42.53.78.62,1.18-.28,1.81A54.6,54.6,0,0,0,71.68,85.32C71.07,86.18,71.05,86.17,70.7,86.15Z"
        />
        <path
          fill="#f39e1f"
          d="M178,76.28c.05.58-.38.7-.69.9-4.27,2.87-8.55,5.72-12.82,8.6-.6.41-1,.47-1.44-.23a54.76,54.76,0,0,0-14-14c-.66-.46-.69-.8-.25-1.45q4.33-6.39,8.59-12.83c.47-.72.82-.84,1.56-.33A74.64,74.64,0,0,1,177.53,75.5C177.72,75.77,177.89,76.06,178,76.28Z"
        />
        <path
          fill="#f39e1f"
          d="M70.68,148.46c.48-.11.59.27.77.52A55.65,55.65,0,0,0,85.59,163.1c.58.4.66.72.26,1.32q-4.38,6.47-8.69,13c-.41.63-.74.81-1.43.32a74.65,74.65,0,0,1-18.8-18.8c-.42-.61-.48-1,.23-1.46,4.34-2.87,8.65-5.78,13-8.67C70.32,148.67,70.52,148.56,70.68,148.46Z"
        />
        <path
          fill="#f39e1f"
          d="M158.24,178.06c-.56-.08-.67-.5-.87-.8-2.84-4.23-5.66-8.47-8.52-12.68-.47-.69-.47-1,.29-1.56A54.46,54.46,0,0,0,163,149.11c.53-.77.9-.7,1.57-.24q6.33,4.29,12.7,8.49c.81.53.86.91.32,1.68a74.06,74.06,0,0,1-18.46,18.45C158.84,177.71,158.5,177.9,158.24,178.06Z"
        />
      </g>
    </g>
  </svg>
);

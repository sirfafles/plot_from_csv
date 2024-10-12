import styles from "./Popup.module.css";

export const Popup = ({ children, visible, setVisible }) => {
  const rootStyles = [styles.popup];
  if (visible) {
    rootStyles.push(styles.active);
  }

  return (
    <div className={rootStyles.join(" ")} onClick={() => setVisible(false)}>
      <div className={styles.popupContent} onClick={(e) => e.stopPropagation()}>
        {children}
      </div>
    </div>
  );
};

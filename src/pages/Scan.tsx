import { FunctionComponent } from "react";
import styles from "./Scan.module.css";

const Scan: FunctionComponent = () => {
  return (
    <div className={styles.scan}>
      <div className={styles.scan1}>
        <div className={styles.div}></div>
        <div className={styles.upload}>Upload</div>
      </div>
      <div className={styles.frame}>
        <div className={styles.camera} />
        <div className={styles.scan2}>
          <div className={styles.div}></div>
          <div className={styles.upload}>Scan</div>
        </div>
      </div>
    </div>
  );
};

export default Scan;

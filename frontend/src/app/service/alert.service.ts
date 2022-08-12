import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { filter } from 'rxjs/operators';
import { Alert } from '../models/alert';
import { AlertOption } from '../models/AlertOption';
import { AlertType } from '../models/alert-type.enum';

@Injectable({
  providedIn: 'root'
})
export class AlertService {
  private subject = new Subject<Alert>();
  private defaultId = 'default-alert';
  // enable subscribing to alert service
  onAlert(id = this.defaultId): Observable<Alert> {
    return this.subject
      .asObservable()
      .pipe(filter((item) => item && item.id === id));
  }

  success(message: string, options?: AlertOption): void {
    this.alert(new Alert({ ...options, type: AlertType.Success, message }));
  }

  info(message: string, options?: AlertOption): void {
    this.alert(new Alert({ ...options, type: AlertType.Info, message }));
  }

  warn(message: string, options?: AlertOption): void {
    this.alert(new Alert({ ...options, type: AlertType.Warning, message }));
  }

  error(message: string, options?: AlertOption): void {
    this.alert(new Alert({ ...options, type: AlertType.Error, message }));
  }

  alert(alert: Alert): void {
    alert.id = alert.id || this.defaultId;
    alert.autoClose = alert.autoClose === undefined ? true : alert.autoClose;
    this.subject.next(alert);
  }

  clear(id = this.defaultId): void {
    this.subject.next(new Alert({ id }));
  }
}

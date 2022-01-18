import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { NavigationStart, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { Alert } from '../models/alert';
import { AlertType } from '../models/alert-type.enum';
import { AlertService } from '../service/alert.service';

@Component({
  selector: 'alert',
  templateUrl: './alert.component.html',
  styleUrls: ['./alert.component.scss']
})
export class AlertComponent implements OnInit, OnDestroy {
  @Input() id = 'default-alert';
  @Input() fade = true;

  alerts: Alert[] = [];
  alertSubscription!: Subscription;
  routeSubscription!: Subscription;
  constructor(private router: Router, private alertService: AlertService) { }

  ngOnInit(){
    // subscribe to new alert notifications
    this.alertSubscription = this.alertService.onAlert(this.id)
          .subscribe(alert => {
            // clear alert when an empty alert is received
            if (!alert.message){
              this.alerts = this.alerts.filter(alert => alert.keepAfterRouteChange);
              this.alerts.forEach(alert => delete alert.keepAfterRouteChange);
              return;
            }
            // add alert to array
            this.alerts.push(alert);

            // auto clear alert if required
            // if (alert.autoClose){
            //   setTimeout(() => this.removeAlert(alert), 5000);
            // }
          });
    this.routeSubscription = this.router.events.subscribe(event => {
      if (event instanceof NavigationStart){
        this.alertService.clear(this.id);
      }
    });
  }


  ngOnDestroy(){
    this.alertSubscription.unsubscribe();
    this.routeSubscription.unsubscribe();
  }
  removeAlert(alert: Alert) {
    if (!this.alerts.includes(alert)) { return; }

    if (this.fade){
      alert.fade = true;
      setTimeout(() => {
        this.alerts = this.alerts.filter(x => x !== alert);
      }, 250);
    } else {
      this.alerts = this.alerts.filter(x => x !== alert);
    }
  }

  cssClasses(alert: Alert) {
    if (!alert) { return; }

    const classes = ['alert', 'alert-dismissable'];

    const alertTypeClass = {
      [AlertType.Success]: 'alert alert-success',
      [AlertType.Info]: 'alert alert-info',
      [AlertType.Warning]: 'alert alert-warning',
      [AlertType.Error]: 'alert alert-danger'
    };

    classes.push(alertTypeClass[alert.type]);
    if (alert.fade){
      classes.push('fade');
    }

    return classes.join(' ');
  }
}

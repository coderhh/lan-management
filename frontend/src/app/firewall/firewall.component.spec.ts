import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { AlertService } from '../service/alert.service';
import { LanService } from '../service/lan.service';

import { FirewallComponent } from './firewall.component';

describe('FirewallComponent', () => {
  let component: FirewallComponent;
  let fixture: ComponentFixture<FirewallComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule, HttpClientTestingModule],
      declarations: [FirewallComponent],
      providers: [LanService, AlertService]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FirewallComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

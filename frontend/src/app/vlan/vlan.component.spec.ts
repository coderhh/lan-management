import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { AlertService } from '../service/alert.service';
import { LanService } from '../service/lan.service';
import { VlanComponent } from './vlan.component';

describe('VlanComponent', () => {
  let component: VlanComponent;
  let fixture: ComponentFixture<VlanComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule, HttpClientTestingModule],
      declarations: [VlanComponent],
      providers: [LanService, AlertService]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(VlanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

/*
 * Copyright 2021-present Open Networking Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package nrl.airman;

import org.apache.karaf.shell.api.action.Command;
import org.apache.karaf.shell.api.action.Argument;

import org.apache.karaf.shell.api.action.lifecycle.Service;
import org.onosproject.cli.AbstractShellCommand;

/**
 * Sample Apache Karaf CLI command.
 */
@Service
@Command(scope = "onos", name = "airman",
         description = "Sample Apache Karaf CLI command")
public class AppCommand extends AbstractShellCommand {
	public static final String CMD_CLEAR_HOST_TABLE = "clear_host_table";
	public static final String CMD_CLEAR_FLOW_TABLE = "clear_flow_table";
	public static final String CMD_CLEAR_SWITCH_TABLE = "clear_switch_table";


	public static final String CMD_CANCEL = "cancel";
	public static final String CMD_HELP = "help";


	@Argument(name = "cmd", description = "command")
    String cmd = null;


    @Override
    protected void doExecute() {
      
        print("Hello %s", "World " + cmd);
        
    	cmd = Optional.ofNullable(cmd).orElse("Error");

		switch (cmd) {
      		case CMD_CLEAR_HOST_TABLE: {
				wipeOutHosts();

        		break;
      		}
			case CMD_CLEAR_FLOW_TABLE: {
				wipeOutFlows();

        		break;
      		}
      		case CMD_CLEAR_SWITCH_TABLE: {
				wipeOutDevices();

    			break;
      		}
      			case CMD_HELP: {
        		break;
			}
      		default: {
        		print("Unknown command %s", commandStr);
        		break;
      		}
    	}
    }
    
    private void wipeOutIntents() {
        print("Wiping intents");
        IntentService intentService = get(IntentService.class);
        Set<Key> keysToWithdrawn = Sets.newConcurrentHashSet();
        Set<Intent> intentsToWithdrawn = Tools.stream(intentService.getIntents())
                .filter(intent -> intentService.getIntentState(intent.key()) != WITHDRAWN)
                .collect(Collectors.toSet());
        intentsToWithdrawn.stream()
                .map(Intent::key)
                .forEach(keysToWithdrawn::add);
        CompletableFuture<Void> completableFuture = new CompletableFuture<>();
        IntentListener listener = e -> {
            if (e.type() == IntentEvent.Type.WITHDRAWN) {
                keysToWithdrawn.remove(e.subject().key());
            }
            if (keysToWithdrawn.isEmpty()) {
                completableFuture.complete(null);
            }
        };
        intentService.addListener(listener);
        intentsToWithdrawn.forEach(intentService::withdraw);
        try {
            if (!intentsToWithdrawn.isEmpty()) {
                // Wait 1.5 seconds for each Intent
                completableFuture.get(intentsToWithdrawn.size() * 1500L, TimeUnit.MILLISECONDS);
            }
        } catch (InterruptedException | ExecutionException | TimeoutException e) {
            print("Encountered exception while withdrawing intents: " + e.toString());
        } finally {
            intentService.removeListener(listener);
        }
        intentsToWithdrawn.forEach(intentService::purge);
    }

    private void wipeOutFlows() {
        print("Wiping Flows");
        FlowRuleService flowRuleService = get(FlowRuleService.class);
        DeviceAdminService deviceAdminService = get(DeviceAdminService.class);
        for (Device device : deviceAdminService.getDevices()) {
            flowRuleService.purgeFlowRules(device.id());
        }
    }

    private void wipeOutGroups() {
        print("Wiping groups");
        GroupService groupService = get(GroupService.class);
        DeviceAdminService deviceAdminService = get(DeviceAdminService.class);
        for (Device device : deviceAdminService.getDevices()) {
            groupService.purgeGroupEntries(device.id());
        }
    }

 
    private void wipeOutHosts() {
        print("Wiping hosts");
        HostAdminService hostAdminService = get(HostAdminService.class);
        while (hostAdminService.getHostCount() > 0) {
            try {
                for (Host host : hostAdminService.getHosts()) {
                    hostAdminService.removeHost(host.id());
                }
            } catch (Exception e) {
                log.info("Unable to wipe-out hosts", e);
            }
        }
    }

    private void wipeOutDevices() {
        print("Wiping devices");
        DeviceAdminService deviceAdminService = get(DeviceAdminService.class);
        while (deviceAdminService.getDeviceCount() > 0) {
            try {
                for (Device device : deviceAdminService.getDevices()) {
                    deviceAdminService.removeDevice(device.id());
                }
            } catch (Exception e) {
                log.info("Unable to wipe-out devices", e);
            }
        }
    }

    private void wipeOutLinks() {
        print("Wiping links");
        LinkAdminService linkAdminService = get(LinkAdminService.class);
        while (linkAdminService.getLinkCount() > 0) {
            try {
                for (Link link : linkAdminService.getLinks()) {
                    linkAdminService.removeLinks(link.src());
                    linkAdminService.removeLinks(link.dst());
                }
            } catch (Exception e) {
                log.info("Unable to wipe-out links", e);
            }
        }
    }

    private void wipeOutPacketRequests() {
        print("Wiping packet requests");
        PacketService service = get(PacketService.class);
        for (PacketRequest r : service.getRequests()) {
            service.cancelPackets(r.selector(), r.priority(), r.appId(), r.deviceId());
        }
    }

  

}

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
import org.apache.karaf.shell.api.action.lifecycle.Service;
import org.onosproject.cli.AbstractShellCommand;

import org.apache.karaf.shell.commands.Command;
import org.onosproject.cli.AbstractShellCommand;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.apache.karaf.shell.commands.Argument;
import org.apache.karaf.shell.commands.Command;
import org.apache.karaf.shell.commands.Option;


import org.onosproject.cli.AbstractChoicesCompleter;
import org.onosproject.cli.AbstractShellCommand;
import org.slf4j.helpers.MessageFormatter;

import com.google.common.collect.Sets;

/*import org.apache.karaf.shell.api.action.Argument;
import org.apache.karaf.shell.api.action.Command;
import org.apache.karaf.shell.api.action.lifecycle.Service;
*/

import org.onlab.util.Tools;
import org.onosproject.cli.AbstractShellCommand;
import org.onosproject.net.Device;
import org.onosproject.net.Host;
import org.onosproject.net.Link;
import org.onosproject.net.config.NetworkConfigService;
import org.onosproject.net.device.DeviceAdminService;
import org.onosproject.net.flow.FlowRuleService;
import org.onosproject.net.group.GroupService;
import org.onosproject.net.host.HostAdminService;
import org.onosproject.net.intent.Intent;
import org.onosproject.net.intent.IntentEvent;
import org.onosproject.net.intent.IntentListener;
import org.onosproject.net.intent.IntentService;
import org.onosproject.net.intent.Key;
import org.onosproject.net.link.LinkAdminService;
import org.onosproject.net.meter.MeterService;
import org.onosproject.net.packet.PacketService;
import org.onosproject.net.packet.PacketRequest;
import org.onosproject.net.region.RegionAdminService;
import org.onosproject.ui.UiExtensionService;
import org.onosproject.ui.UiTopoLayoutService;
import org.onosproject.net.host.HostService;
import java.util.Set;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import java.util.stream.Collectors;

import java.util.ArrayList;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

import org.apache.commons.lang.math.RandomUtils;
import org.onlab.packet.MacAddress;
import org.onosproject.cli.AbstractShellCommand;
import org.onosproject.core.ApplicationId;
import org.onosproject.core.CoreService;
import org.onosproject.net.Device;
import org.onosproject.net.PortNumber;
import org.onosproject.net.device.DeviceService;
import org.onosproject.net.flow.DefaultFlowRule;
import org.onosproject.net.flow.DefaultTrafficSelector;
import org.onosproject.net.flow.DefaultTrafficTreatment;
import org.onosproject.net.flow.FlowEntry.FlowEntryState;
import org.onosproject.net.flow.FlowRule;
import org.onosproject.net.flow.FlowRuleOperations;
import org.onosproject.net.flow.FlowRuleOperationsContext;
import org.onosproject.net.flow.FlowRuleService;
import org.onosproject.net.flow.TrafficSelector;
import org.onosproject.net.flow.TrafficTreatment;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.google.common.base.Stopwatch;
import com.google.common.collect.Iterables;
import com.google.common.collect.Lists;
import com.google.common.collect.Streams;

import static org.onosproject.net.intent.IntentState.WITHDRAWN;
import static com.google.common.collect.Lists.newArrayList;


/**
 * Sample Apache Karaf CLI command.
 */
@Service
@Command(scope = "onos", name = "sample",
         description = "Sample Apache Karaf CLI command")
public class AppCommand extends AbstractShellCommand {
	public static final String CMD_FLOOD_FLOW_TABLE = "flood_flow_table";

	public static final String CMD_CANCEL = "cancel";
	public static final String CMD_HELP = "help";


	// Arguments/Options
	@Argument(index = 0, name = "command", required = true,
		description = "name of the command")
	private String commandStr = null;

	@Argument(index = 1, name = "param...", required = false, multiValued = true,
		description = "param(s) required by commands")
	private List<String> paramList = new ArrayList<>();


    @Override
    protected void doExecute() {
      
        print("Hello %s", "World");
        
        commandStr = Optional.ofNullable(commandStr).orElse("Error");

		switch (commandStr) {

		  	case CMD_FLOOD_FLOW_TABLE: {
				print ("attack flood flow table: " + attackFloodFlowTable());
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
    
    
    private CountDownLatch latch;
	private String attackFloodFlowTable() {
	    int MAX_OUT_PORT = 254;
		if (paramList.size() != 2) {
			return "usage: switchIndex numFlows";
		}

		int flowsPerDevice = Integer.parseInt(paramList.get(0));
		int num = Integer.parseInt(paramList.get(1));

		FlowRuleService flowService = get(FlowRuleService.class);
        DeviceService deviceService = get(DeviceService.class);
        CoreService coreService = get(CoreService.class);

       	ApplicationId appId = coreService.registerApplication("onos.test.flow.installer");

       
        ArrayList<Long> results = Lists.newArrayList();
        Iterable<Device> devices = deviceService.getDevices();
        TrafficTreatment treatment = DefaultTrafficTreatment.builder()
                .setOutput(PortNumber.portNumber(RandomUtils.nextInt(MAX_OUT_PORT))).build();
        TrafficSelector.Builder sbuilder;
        FlowRuleOperations.Builder rules = FlowRuleOperations.builder();
        FlowRuleOperations.Builder remove = FlowRuleOperations.builder();

        for (Device d : devices) {
            for (long i = 0; i < flowsPerDevice; i++) {
                sbuilder = DefaultTrafficSelector.builder();

                sbuilder.matchEthSrc(MacAddress.valueOf(RandomUtils.nextInt() * i))
                        .matchEthDst(MacAddress.valueOf((Integer.MAX_VALUE - i) * RandomUtils.nextInt()));


                int randomPriority = RandomUtils.nextInt(
                        FlowRule.MAX_PRIORITY - FlowRule.MIN_PRIORITY + 1) + FlowRule.MIN_PRIORITY;

                FlowRule addRule = DefaultFlowRule.builder()
                        .forDevice(d.id())
                        .withSelector(sbuilder.build())
                        .withTreatment(treatment)
                        .withPriority(randomPriority)
                        .fromApp(appId)
                        .makeTemporary(10)
                        .build();
                FlowRule removeRule = DefaultFlowRule.builder()
                        .forDevice(d.id())
                        .withSelector(sbuilder.build())
                        .withTreatment(treatment)
                        .withPriority(randomPriority)
                        .fromApp(appId)
                        .makeTemporary(10)
                        .build();

                rules.add(addRule);
                //remove.remove(removeRule);

            }
        }
        // close stages
        rules.newStage();
        remove.newStage();

        for (int i = 0; i < num; i++) {
            printProgress("Run %d:", i);
            latch = new CountDownLatch(2);
            final CountDownLatch addSuccess = new CountDownLatch(1);
            printProgress("..batch add request");
            Stopwatch add = Stopwatch.createStarted();

            flowService.apply(rules.build(new FlowRuleOperationsContext() {

                private final Stopwatch timer = Stopwatch.createStarted();

                @Override
                public void onSuccess(FlowRuleOperations ops) {

                    timer.stop();
                    printProgress("..add success");
                    results.add(timer.elapsed(TimeUnit.MILLISECONDS));
                    if (results.size() == num) {
                       
                            printTime(true, results);
                       
                    }
                    latch.countDown();
                    addSuccess.countDown();
                }
            }));

if (false) {

            try {
                addSuccess.await();
                // wait until all flows reaches ADDED state
                while (!Streams.stream(flowService.getFlowEntriesById(appId))
                        .allMatch(fr -> fr.state() == FlowEntryState.ADDED)) {
                    Thread.sleep(100);
                }
                add.stop();
                printProgress("..completed %d ± 100 ms", add.elapsed(TimeUnit.MILLISECONDS));
            } catch (InterruptedException e1) {
                printProgress("Interrupted");
                Thread.currentThread().interrupt();
            }

            printProgress("..cleaning up");
            flowService.apply(remove.build(new FlowRuleOperationsContext() {
                @Override
                public void onSuccess(FlowRuleOperations ops) {
                    latch.countDown();
                }
            }));

            try {
                latch.await();
                while (!Iterables.isEmpty(flowService.getFlowEntriesById(appId))) {
                    Thread.sleep(500);
                }
            } catch (InterruptedException e) {
                printProgress("Interrupted.");
                Thread.currentThread().interrupt();
            }
        }

}
		
		return "added " + flowsPerDevice + " to switchIndex " + num;

	}

  private void printProgress(String format, Object... args) {
        
            print(format, args);
    }


    private void printTime(boolean isSuccess, ArrayList<Long> elapsed) {
        print("Run is %s.", isSuccess ? "success" : "failure");
        for (int i = 0; i < elapsed.size(); i++) {
            print("  Run %s : %s ms", i, elapsed.get(i));
        }
    }

}

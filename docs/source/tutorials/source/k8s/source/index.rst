.. _k8s:

srsRAN gNB on Kubernetes
########################

Introduction
************

This tutorial outlines the steps required to launch the srsRAN gNB with `Kubernetes <https://kubernetes.io/>`_.
This is a useful tool for use-cases that require users to deploy and manage networks over a prolonged period,
with high levels of guaranteed service ability and enhanced fault tolerance.

In short, Kubernetes can be described as the following:

   *When it comes to managing test networks, the adoption of Kubernetes
   is pivotal for streamlined and efficient operations. Kubernetes provides
   a unified platform for orchestrating diverse functions within the network,
   optimizing resource utilization, and automating scaling based on demand. Its
   inherent capability to enhance fault tolerance ensures consistent service availability,
   while the ease of continuous deployment supports rapid innovation. Kubernetes also excels
   in simplifying the deployment process across various environments, fostering adaptability.
   In essence, Kubernetes emerges as a practical solution, offering a cohesive and scalable 
   framework for effective network function management.*

Such deployments may not be suited to more research and development focused use-cases that
require fine-tuning of configuration files and development of source-code. Iterative development
and testing is more suited to "bare metal" deployments.

Further Reading
================

We recommend unexperienced users read the following two articles before starting with this tutorial:

   - `Getting started with Kubernetes <https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/>`_
   - `Getting started with Helm <https://helm.sh/docs/intro/>`_

-----

Setup Considerations
********************

.. image:: .imgs/k8s.png
    :width: 75%
    :align: center

This tutorial we will cover the following topics:

    - Set up K8s/K3s nodes
        - Install realtime kernel
        - Tune system performance via TuneD
        - Install DPDK
        - Install and configure the SR-IOV plugin
    - Set up PTP syncronization
        - LLS-C1 and LLS-C3
    - Set up core network Open5gs
    - Set up gNB
        - Connecting to cluster external core networks and SMOs using a LoadBalancer
        - Connecting to cluster internal core networks and SMOs
        - Assing DPDK devices using SR-IOV plugin
        - Assing DPDK devices without SR-IOV plugin
        - Using srsRAN Project with a SMO
    - Run load testing
        - cyclictest
        - srsRAN RU Emulator
    - Visualizing KPIs via Grafana

In this tutorial we will be using a single node cluster based on Ubuntu 24.04. We
require at least Kubernetes version 1.24 or newer. Also, this tutorial requires a
basic understanding of Kubernetes and Helm.

CU/DU
=====

The CU/DU is provided by the srsRAN Project gNB. The Open Fronthaul
(OFH) Library provides the necessary interface between the DU and the
RU.

RU
===

For this tutorial you can use every of the RUs supported by the srsRAN. For more information on
supported O-RUs, see :ref:`this section <hw_integration>` of the RU tutorial.

5G Core
=======

For this tutorial we use the Open5GS 5G Core.

Open5GS is a C-language open-source implementation for 5G Core and EPC.
The following links will provide you with the information needed to
download and setup Open5GS so that it is ready to use with srsRAN:

   - `Open5GS GitHub <https://github.com/open5gs/open5gs>`_
   - `Open5GS Quickstart Guide <https://open5gs.org/open5gs/docs/guide/01-quickstart/>`_

Clocking & Synchronization
==========================

The split 7.2 interface requires tight timing synchronization between
the DU and RU. O-RAN WG 4 has defined various synchronization methods
for use with Open Fronthaul. These are outlined in
O-RAN.WG4.CUS.0-R003-v11.00 Section 11.

In this tutorial we explain how to set up LLS-C1 or LLS-C3 configruation.
The LLS-C1 configuration is used when the DU is the PTP grandmaster and the RU is the
PTP client. The LLS-C3 configuration is used when both, DU and RU are PTP client.
The PTP grandmaster is usually a GPS clock or a Rubidium clock. The PTP client is
usually a network interface card (NIC) that supports PTP.

----------

Set up a K8s/K3s bare metal cluster
***********************************

1. Deploy a Kubernetes cluster
==============================

For the installation of Kubernetes varies accross distributions and tools to be used for the deployment. Depending
on your needs and the environment you are deploying to, you can choose the tool that best fits your needs. For this
guide, we will be deploying a single node K3s cluster on Ubuntu 24.04. K3s is lightweight and easy to set up. It is
a fully compliant Kubernetes distribution that is easy to install and manage. It is designed for resource-constrained
environments and edge computing. K3s is a great choice for deploying Kubernetes on bare metal servers.

Some tools that can be used to deploy K8s are:

- `Kubespray <https://kubespray.io/>`_
- `kubeadm <https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/>`_
- `K3s <https://k3s.io/>`_
- `Rancher <https://rancher.com/>`_

The installation of K3s is very simple and can be done with a single command. The following command will install
K3s on your server:

.. code-block:: bash

    curl -sfL https://get.k3s.io | sh -

For more information on how to install K3s, you can refer to the `official documentation <https://k3s.io/>`_.

2. Install realtime kernel
==========================

The real-time kernel in Ubuntu 24.04 LTS, built on the PREEMPT_RT patch, ensures low-latency and deterministic
performance for time-sensitive operations. By prioritizing critical processes and providing predictable response
times, it is ideal for industries like manufacturing, automotive, and telecommunications. This release also
enhances support for Raspberry Pi hardware, enabling optimized real-time computing across diverse applications.

To install the real-time kernel on Ubuntu 24.04 you need to get a free Canonical Pro subscription. Therefore,
register on the `Canonical website <https://ubuntu.com/pro>`_ and create an account. After that, you can obtain
a Pro token and use the following commands to install the real-time kernel:

.. code-block:: bash

    sudo pro attach <your-token>
    sudo pro enable realtime-kernel

Reboot the system after the installation has finsihed. For more inforamtion refer to the
`Ubuntu documentation <https://documentation.ubuntu.com/pro-client/en/docs/howtoguides/enable_realtime_kernel/>`_.

3. Install TuneD
================

For the performance tuning with TuneD please refer to the :ref:`srsRAN Performance Tuning Guide <_tuning>` in our documentation.

4. Install DPDK
===============

For the installation of DPDK please refer to the :ref:`srsRAN documentation <_dpdk>`.

5. Install and configure the SR-IOV plugin
==========================================

.. _sriov_plugin:

The SR-IOV plugin is a Kubernetes plugin that enables the use of SR-IOV devices in Kubernetes. It allows you to
dynamically assign virtual functions (VFs) to Pods. This allows you to use SR-IOV devices in Kubernetes without
priviledged access to the host.

In the following example we will use the `SR-IOV CNI plugin <https://github.com/k8snetworkplumbingwg/sriov-cni>`_ and `MULTUS <https://github.com/k8snetworkplumbingwg/multus-cni#quickstart-installation-guide>`_

5.1 Configure Virtual Functions (VFs)
-------------------------------------

As a first step we enable a single Virtual Functions (VFs) on the host, change its MAC and bind it to the vfio-pci
driver for DPDK. In our example the VF is created for interface named ``enp1s0f0``. For more information refert to
the `DPDK tutorial of our srsRAN Documentation <https://docs.srsran.com/projects/project/en/latest/tutorials/source/dpdk/source/index.html>`_

.. code-block:: bash

    # Enable VF
    echo 1 > /sys/class/net/enp1s0f0/device/sriov_numvfs
    # Change MAC address
    ip link set enp1s0f0 vf 0 mac 00:11:22:33:44:55
    # Bind VF to vfio-pci
    dpdk-devbind.py -b vfio-pci 0000:01:01.0

5.2 Edit and Apply ConfigMap
----------------------------

In this step we create the necessary configMap.yaml for the SR-IOV CNI plugin. The configMap.yaml file contains
the device vendor and and device ID of the NIC. The device ID can be found using the ``lspci`` command as shown
below. Its important to note that PFs and VFs have different device IDs.

.. code-block:: bash

    lspci -nn -s 01:01.0 
    01:01.0 Ethernet controller [0200]: Intel Corporation Ethernet Adaptive Virtual Function [8086:1889] (rev 02)

In our case the device ID is ``1889`` and the vendor ID is ``8086``. The configMap.yaml file should look like this:

.. code-block:: yaml

    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: sriovdp-config
      namespace: kube-system
    data:
      config.json: |
         {
              "resourceList": [{
                         "resourceName": "intel_sriov_netdevice",
                         "selectors": {
                              "vendors": ["8086"],
                              "devices": ["1889"],
                              "drivers": ["vfio-pci"]
                         }
                    }
                 ]
         }

Save and apply the configMap using the following command:

.. code-block:: bash

    kubectl apply -f configMap.yaml

5.3 Install Multus CNI
----------------------

Deploy Multus CNI using the following command:

.. code-block:: bash

    kubectl apply -f https://raw.githubusercontent.com/k8snetworkplumbingwg/multus-cni/master/deployments/multus-daemonset-thick.yml

For more information on the installation of the Multus plugin have a look at the 
`installation guide <https://github.com/k8snetworkplumbingwg/multus-cni#quickstart-installation-guide>`_


5.4 Install SR-IOV Components
-----------------------------

Install the following 3 components to enable SR-IOV in the k3s cluster. Make sure all of the daemonsets
are properly defined for your cluster.

- Install the SR-IOV CNI plugin and its DaemonSet:

.. code-block:: bash

    kubectl apply -f sriov-cni-daemonset.yaml

- Install the SR-IOV Custom Resource Definitions (CRDs):

.. code-block:: bash

    kubectl apply -f sriov-crd.yaml

- Install the SR-IOV Device Plugin DaemonSet:

.. code-block:: bash

    kubectl apply -f sriovdp-daemonset.yaml

The SR-IOV plugin is a Kubernetes plugin that enables the use of SR-IOV devices in Kubernetes.
(`SR-IOV Network Device Plugin <https://github.com/k8snetworkplumbingwg/sriov-network-device-plugin>`_)
It allows you to dynamically assign virtual functions (VFs) to Pods. This allows you to use SR-IOV devices
in Kubernetes without priviledged access to the host.

In the following example we will use the `SR-IOV CNI plugin <https://github.com/k8snetworkplumbingwg/sriov-cni>`_ and `MULTUS <https://github.com/k8snetworkplumbingwg/multus-cni#quickstart-installation-guide>`_

5.1 Configure Virtual Functions (VFs)
-------------------------------------

As a first step we enable a single Virtual Functions (VFs) on the host, change its MAC and bind it to the
vfio-pci driver for DPDK. In our example the VF is created for interface named ``enp1s0f0``. For more information
refert to the `DPDK tutorial of our srsRAN Documentation <https://docs.srsran.com/projects/project/en/latest/tutorials/source/dpdk/source/index.html>`_.

.. code-block:: bash

    # Enable VF
    echo 1 > /sys/class/net/enp1s0f0/device/sriov_numvfs
    # Change MAC address
    ip link set enp1s0f0 vf 0 mac 00:11:22:33:44:55
    # Bind VF to vfio-pci
    dpdk-devbind.py -b vfio-pci 0000:01:01.0

5.2 Edit and Apply ConfigMap
----------------------------

In this step we create the necessary configMap.yaml for the SR-IOV CNI plugin. The configMap.yaml file
contains the device vendor and and device ID of the NIC. The device ID can be found using the ``lspci``
command as shown below. Its important to note that PFs and VFs have different device IDs.

.. code-block:: bash

    lspci -nn -s 01:01.0 
    01:01.0 Ethernet controller [0200]: Intel Corporation Ethernet Adaptive Virtual Function [8086:1889] (rev 02)

In our case the device ID is ``1889`` and the vendor ID is ``8086``. The configMap.yaml file should look like this:

.. code-block:: yaml

    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: sriovdp-config
      namespace: kube-system
    data:
      config.json: |
         {
              "resourceList": [{
                         "resourceName": "intel_sriov_netdevice",
                         "selectors": {
                              "vendors": ["8086"],
                              "devices": ["1889"],
                              "drivers": ["vfio-pci"]
                         }
                    }
                 ]
         }

Save and apply the configMap using the following command:

.. code-block:: bash

    kubectl apply -f configMap.yaml

5.3 Install Multus CNI
----------------------

Deploy Multus CNI using the following command:

.. code-block:: bash

    kubectl apply -f https://raw.githubusercontent.com/k8snetworkplumbingwg/multus-cni/master/deployments/multus-daemonset-thick.yml

For more information on the installation of the Multus plugin have a look at the
`installation guide <https://github.com/k8snetworkplumbingwg/multus-cni#quickstart-installation-guide>`_


5.4 Install SR-IOV Components
-----------------------------

Install the following 3 components to enable SR-IOV in the k3s cluster. Make sure all of the daemonsets are
properly defined for your cluster.

- Install the SR-IOV CNI plugin and its DaemonSet:

.. code-block:: bash

    kubectl apply -f sriov-cni-daemonset.yaml

- Install the SR-IOV Custom Resource Definitions (CRDs):

.. code-block:: bash

    kubectl apply -f sriov-crd.yaml

- Install the SR-IOV Device Plugin DaemonSet:

.. code-block:: bash

    kubectl apply -f sriovdp-daemonset.yaml

.. todo::
    Attach 3 manifest files

----------

Set up PTP synchronization
**************************

We have created a Helm chart to deploy ptp4l, phc2sys and ts2phc for PTP synchronization. As a first step install the
srsRAN Project Helm repository:

.. code-block:: bash

    helm repo add srsran https://srsran.github.io/srsRAN_Project_helm/

Depending on your setup the deployment of the PTP components can be done in different ways. The most common configurations
are either LLS-C1 or LLS-C3 using either uni-cast or multicast transmission (https://www.techplayon.com/o-ran-fronthaul-transport-synchronization-configurations/).
In the LLS-C1 configuration the DU server is driving the PTP synchronization and the RU is configured as a client. The RU
is only receiving the PTP messages from the DU server. In the LLS-C3 configuration both, DU and RU are configured as clients
and are receiving the PTP messages from a PTP grandmaster.

In this tutorial we will show how to deploy both, LLS-C1 and LLS-C3 configurations using the G.8275.1 multicast profile of
linuxptp. For more information on LinuxPTP refer to the official documentation (https://linuxptp.nwtime.org/documentation/).
The configuration of the Helm chart needs to be done in the values.yaml file.

LLS-C1 example configuration:

.. code-block:: yaml

    config:
        dataset_comparison: "G.8275.x"
        G.8275.defaultDS.localPriority: "128"
        maxStepsRemoved: "255"
        logAnnounceInterval: "-3"
        logSyncInterval: "-4"
        logMinDelayReqInterval: "-4"
        serverOnly: "1"
        clientOnly: "0"
        G.8275.portDS.localPriority: "128"
        ptp_dst_mac: "01:80:C2:00:00:0E"
        network_transport: "L2"
        domainNumber: "24"

LLS-C3 example configuration:

.. code-block:: yaml

    config:
        dataset_comparison: "G.8275.x"
        G.8275.defaultDS.localPriority: "128"
        maxStepsRemoved: "255"
        logAnnounceInterval: "-3"
        logSyncInterval: "-4"
        logMinDelayReqInterval: "-4"
        serverOnly: "0"
        clientOnly: "1"
        G.8275.portDS.localPriority: "128"
        ptp_dst_mac: "01:80:C2:00:00:0E"
        network_transport: "L2"
        domainNumber: "24"

For more information on the configuration of the values.yaml file of the linuxptp helm chart please refer to
its readme (https://github.com/srsran/srsRAN_Project_helm/tree/main/charts/linuxptp). An example of the linuxptp
values.yaml file can be obtained here: https://raw.githubusercontent.com/srsran/srsRAN_Project_helm/main/charts/linuxptp/values.yaml.
The deployment of the PTP components can be done using the following command:

.. code-block:: bash

    helm install ptp4l srsran/linuxptp -f values.yaml

If the server is under high load and the PTP quality degrades you can give the linuxptp Pod an exclusive CPU
core by editing the resources section of the values.yaml file. This will ensure that the linuxptp Pod is not
affected by other Pods running on the server. The resources section should look like this:

.. code-block:: yaml

    resources:
        requests:
        cpu: "1"
        memory: "512Mi"
        limits:
        cpu: "1"
        memory: "512Mi"

----------

Set up core network Open5gs
***************************

Open5GS is a C-language open-source implementation for 5G Core and EPC. The following links will provide you
with the information needed to download and setup Open5GS so that it is ready to use with srsRAN:

- Open5GS GitHub: https://github.com/open5gs/open5gs
- Open5GS Quickstart Guide: https://open5gs.org/open5gs/docs/guide/01-quickstart/

As a first step install the Open5GS Helm repo from Gradiant:

.. code-block:: bash

    helm pull oci://registry-1.docker.io/gradiant/open5gs --version 2.2.0

For the deployment edit the values.yaml file and set the desired RAN parameters. An example of the Open5GS Helm
Chart values.yaml can be found here: https://gradiant.github.io/openverso-charts/docs/open5gs-ueransim-gnb/5gSA-values.yaml.

Deploy Open5GS using the following command:

.. code-block:: bash

    helm install open5gs oci://registry-1.docker.io/gradiant/open5gs --version 2.2.0 -f 5gSA-values.yaml -n open5gs --create-namespace --set mongodb.persistence.enabled=false

This command deploys Open5GS in the open5gs namespace. The --set mongodb.persistence.enabled=false flag is
used to disable the persistence of the MongoDB database. This is useful for testing purposes, but in a
production environment you should enable persistence. You can enable persistance by setting up a PV and
PVC in your cluster and make the mongodb Pod use it. For more information on how to set up a PV and PVC
refer to the Kubernetes documentation (https://kubernetes.io/docs/concepts/storage/persistent-volumes/).

You should see the following output:

.. code-block:: bash

    Pulled: registry-1.docker.io/gradiant/open5gs:2.2.0
    Digest: sha256:99d49ab6bb2d4a5c78be31dd2c3a99a0780de79bd22d0bfa9df734ca2705940a
    NAME: open5gs
    LAST DEPLOYED: Mon Dec  9 11:09:17 2024
    NAMESPACE: open5gs
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None

Wait until all Pods are running. You can check the status with the following command:

.. code-block:: bash

    kubectl get pods -n open5gs

Once all components are started and running you can edit the subscribers via the Open5GS WebUI. For that, you
need to forward port 9999 of the open5gs-webui service to your local machine:

.. code-block:: bash

    kubectl port-forward svc/open5gs-webui 9999:9999 -n open5gs

You should see the following output:

.. code-block:: bash

    Forwarding from 127.0.0.1:9999 -> 9999
    Forwarding from [::1]:9999 -> 9999

Don't close the shell and open your browser at http://localhost:9999. (Username: admin, Password: 1423). Once
you are logged in you can edit the subscribers. After setting up the subscribers you can close the shell.

Set up gNB
**********

For the deployment edit the values.yaml file and set the desired RAN parameters. An example of the srsRAN
Project Helm Chart values.yaml can be found here: https://raw.githubusercontent.com/srsran/srsRAN_Project_helm/main/charts/srsran-project/values.yaml.

If you havent already added the srsRAN Project Helm repo, install it using the following command:

.. code-block:: bash

    helm repo add srsran https://srsran.github.io/srsRAN_Project_helm/

In the follwoing we wil explain how to set up different scenarios using the srsRAN Helm Chart.

1 Connecting to cluster external core networks and SMOs using a LoadBalancer
============================================================================

In this scenario we will connect the gNB to an external core network or SMO using a LoadBalancer. The
LoadBalancer will be used to expose the gNB to the outside world. In bare metal Kubernetes clusters the
LoadBalancer needs to be installed manually. For K8s you can use for example MetalLB (https://metallb.io/),
in K3s the LoadBalancer is already installed.

In order to deploy the gNB via Helm for the use with a LoadBalancer, make sure the following configuration is
set in the values.yaml:

Make sure the access to the hosts network is disabled:

.. code-block:: yaml

    network:
        hostNetwork: false

For connecting to an cluster external core network set up the LoadBalancer IP address and N2 and N3 IP address.
In case N2 and N3 binds to the same interface, use the same IP for both ports. Make sure that the IP assigned to
the LoadBalancer matches the IP in LoadBalancerIP:

.. code-block:: yaml

    service:
        type: LoadBalancer
        LoadBalancerIP: "192.168.30.30"
        ports:
        n2:
            port: 38412
            outport: 38412
            protocol: SCTP
        n3:
            port: 2152
            outport: 32152
            protocol: UDP

For an external SMO use the following configuration:

.. code-block:: yaml

    service:
        type: LoadBalancer
        LoadBalancerIP: "192.168.30.30"
        ports:
        o1:
            port: 830
            outport: 830
            protocol: TCP

2 Connecting to cluster internal core networks and SMOs
=======================================================

When all components are running in the same cluster we can use host names instead of a LoadBalancer. In case
the Open5GS core network is running in the same cluster we can use the hostname of the AMF to connect to it
instead of using the Pod's or service's IP address. In order to derive the hostname of the service we need
to obtain the cluster domain first. Use the following commands to do so:

.. code-block:: bash

    kubectl run -it --image=ubuntu --restart=Never shell -- sh -c 'apt-get update > /dev/null && apt-get install -y dnsutils > /dev/null && nslookup kubernetes.default | grep Name | sed "s/Name:\skubernetes.default//"'

This command creates a Pod, installs some tools and runs a DNS query against the service kubernetes.default. The output should look like this:

.. code-block:: bash

    If you don't see a command prompt, try pressing enter.
    debconf: delaying package configuration, since apt-utils is not installed

    .svc.kubernetes.local

In this case the cluster domain is svc.kubernetes.local. To now get the hostname of the service append the
service name and the namespace to the cluster domain in the following manner:

.. code-block:: bash

    my-svc.my-namespace.svc.cluster-domain.example

You can get all services names using the following command:

.. code-block:: bash

    kubectl get services -A
    NAMESPACE     NAME               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                  AGE
    default       kubernetes         ClusterIP   10.96.0.1        <none>        443/TCP                  10d
    default       open5gs-amf-ngap   ClusterIP   10.111.110.41    <none>        38412/SCTP               16h
    [...]

The Open5GS AMF service name is ``open5gs-amf`` and the namespace is ``default``. Therefore the hostname of the AMF service is ``open5gs-amf-ngap.default.svc.kubernetes.local``. Use this hostname in the gNB config section of the Helm chart for the AMF.

For more information please refer to the official Kubernetes documentation: https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/

3 Assing DPDK devices using SR-IOV plugin
=========================================

When using the SR-IOV plugin you can assign DPDK devices to the gNB using the following configuration in the values.yaml file:

Set the following values in the secuirtyContext:

.. code-block:: yaml

    securityContext:
        allowPrivilegeEscalation: false
        capabilities:
        add:
            - IPC_LOCK
            - SYS_ADMIN
            - SYS_RAWIO
            - NET_RAW
            - SYS_NICE
        privileged: false

Before the deployment make sure that the SR-IOV plugin is installed and the VFs are created. For more information
on how to set up the SR-IOV plugin refer to the :ref:`section above <_sriov_plugin>`. You can check if the node has available SR-IOV
devices using the following command:

.. code-block:: bash

    kubectl describe node <node-name>

Depending on how you have named the SR-IOV device in the configmap, it will show up under a different name int he resource section. You
should see the following output:

.. code-block:: yaml

    resources:
      enable_hugepages_1gi: true
      requests:
        hugepages-1Gi: 2Gi
        cpu: 12
        memory: 16Gi
        intel.com/intel_sriov_netdevice: '1'
      limits:
        hugepages-1Gi: 2Gi
        memory: 16Gi
        cpu: 12
        intel.com/intel_sriov_netdevice: '1'

As you can see in the console snippet on DPDK device is available on the system.

4 Assing DPDK devices without SR-IOV plugin
===========================================

In order to assign PFs or VF directly to the container without the SR-IOV plugin you need to give the Pod full
access to the host system. Therefore, make sure the following settings are set in the values.yaml file:

Make sure the access to the hosts network is enabled:

.. code-block:: yaml

    network:
        hostNetwork: true

Enable priviledged access to the host and set the two capabilites below:

.. code-block:: yaml

    securityContext:
        capabilities:
        add: ["SYS_NICE", "NET_ADMIN"]
        privileged: true

Using this configuration the gNB Pod has access to the network stack of the host. That means you can access
everything host can access, but also everything inside the Kubernetes cluster the Pod is running in.

5 Using srsRAN Project with a SMO
=================================

To enable the O1 interface in the gNB use the following configuration in your values.yaml:

.. code-block:: yaml

    o1:
        enable_srs_o1: true
        netconfServerAddr: "localhost"
        o1Port: 830
        healthcheckPort: 5000
        o1Adapter:
        image: softwareradiosystems/srsran_5g_enterprise/o1_adapter
        repository: registry.gitlab.com
        pullPolicy: IfNotPresent
        tag: latest
        resources: {}
        securityContext: {}
        netconfServer:
        image: softwareradiosystems/srsran_5g_enterprise/netconf
        repository: registry.gitlab.com
        pullPolicy: IfNotPresent
        tag: latest
        resources: {}
        securityContext: {}

The netconfServerAddr should be set to localhost in case the srsRAN netconf server is used. Set this address in
case you want to use an external netconf server. Currently, the external netconf server is not supported via
LoadBalancer, you have to use a configuration as described in the section ### 4 Assing DPDK devices without SR-IOV plugin.

.. todo::
    Provide example configs for 1-5

Load testeing
*************

In the following we will present two methods to test the maximum load on the system.

1 srsRAN RU Emulator
====================

The srsRAN RU Emulator is a tool that emulates a Radio Unit (RU). It prints KPIs like early and late packets. This
can help to debug problems in networks. It also helps to evaluate how much load deployments can handle. You can
quickly deploy the RU Emulator by using the RU Emulator Helm chart.

For deploying the RU Emulator we first need to obtain the RU and DU MAC address, as well as the bandwidth,
VLAN tag and the compression. These parameters are mandetory. The ru_mac_addr is the MAC of the interface to be 
used for the OFH traffic, the du_mac_addr field sets the MAC address of the DU interface used for OFH traffic.

.. code-block:: yaml

    ru_emu:
        cells:
        - bandwidth: 100
        network_interface: enp4s0f0
        ru_mac_addr: 50:7c:6f:45:44:33
        du_mac_addr: 00:11:22:33:44:00
        vlan_tag: 6
        ul_port_id: [0]
        compr_method_ul: "bfp"
        compr_bitwidth_ul: 9

Depending on if you are using the SR-IOV plugin or not, you need to update the securityContext. In case you want to use the SR-IOV plugin
you need to set the following values in the securityContext. The network_interface and the du_mac_addr will be replaced at runtime with
the correct values.

.. code-block:: yaml

    securityContext:
        allowPrivilegeEscalation: false
        capabilities:
        add:
            - IPC_LOCK
            - SYS_ADMIN
            - SYS_RAWIO
            - NET_RAW
            - SYS_NICE
        privileged: false

Use the following secuirtyContext if you dont want to use the SR-IOV plugin. Make sure network_interface and du_mac_addr are set to
the correct values.

.. code-block:: yaml

    securityContext:
        capabilities:
        add: ["SYS_NICE", "NET_ADMIN"]
        privileged: true 

.. todo::
    Implement SR-IOV support for RU Emulator.

2 Asses max latency using cyclictest
====================================

cyclictest is a tool to asses the latency of applications on real time systems?

.. todo::
    How does it work? Example config? Tests outputs? Picture of the generated graph

----------

Visualizing KPIs via Grafana
****************************

To visualize the gNB KPIs we have created a Grafana dashboard. The dashboard is designed to work with the
metrics server that is part of the srsRAN Project Helm repository. The metrics server collects metrics from
the gNB, parses and stores them in an InfluxDB database. The Grafana dashboard queries the InfluxDB database
to display the metrics in a user-friendly way.

In order to install the Grafana Helm Chart make sure you have added the srsRAN Helm repository to your Helm
repositories. If you haven't done this yet, use the following command:

.. code-block:: bash

    helm repo add srsran https://srsran.github.io/srsRAN_Project_helm/

The dashboard comes with a pre-configured values.yaml file. The only option that needs to be adjusted is the cluster
domain to properly resolve the hostnames used in this tutorial. To get the your cluster domain you can use the following command:

.. code-block:: bash

    kubectl run -it --image=ubuntu --restart=Never shell -- sh -c 'apt-get update > /dev/null && apt-get install -y dnsutils > /dev/null && nslookup kubernetes.default | grep Name | sed "s/Name:\skubernetes.default//"'

This command creates a Pod, installs some tools and runs a DNS query against the service kubernetes.default. The output should look like this:

.. code-block:: bash

    If you don't see a command prompt, try pressing enter.
    debconf: delaying package configuration, since apt-utils is not installed

    .svc.kubernetes.local

In this case the cluster domain is svc.kubernetes.local. Adjust the values.yaml file to reflect your cluster domain.
Get the default values.yaml file with the following command:

.. code-block:: bash

    wget https://raw.githubusercontent.com/srsran/srsRAN_Project_helm/refs/heads/main/charts/grafana-srsran/values.yaml

In the default values.yaml file the cluster domain is set to .svc.cluster.local. Replace the two occurrences of 
.svc.cluster.local with the string returned in the last step. The metrics server section looks like this after 
replacing the default cluster domain:

.. code-block:: bash

    metrics-server:
        config:
        port: 55555
        bucket: srsran
        testbed: default
        url: http://grafana-influxdb.srsran.svc.kubernetes.local
        org: srs
        token: "605bc59413b7d5457d181ccf20f9fda15693f81b068d70396cc183081b264f3b"
        serviceType: "ClusterIP"

After that, you can remove the test container using this command:

.. code-block:: bash

    kubectl delete pod shell

Adjust the values.yaml to correct the cluster domain. After that, deploy the Grafana dashboard with the following command:

.. code-block:: bash

    helm install srsran-grafana srsran/grafana-deployment -f values.yaml -n srsran --create-namespace

Once all components are up, the gNB application can start sending traffic to the metrics server. To access the Grafana dashboard, 
you need to forward the port of the Grafana service to your local machine. Use the following commands to forward the port. Make 
sure the namespaces is set correctly.

.. code-block:: bash

    export POD_NAME=$(kubectl get pods --namespace srsran -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=srsran-grafana" -o jsonpath="{.items[0].metadata.name}")
    kubectl --namespace srsran port-forward $POD_NAME 3000

After that you can access the grafana dashboard by opening your browser at http://localhost:3000. An example of the Grafana dashboard is shown below:

----------

Clean up deployments
********************

To clean up all deployments, use the following commands:

.. code-block:: bash

    helm uninstall srsran-project -n srsran

To delete the LinuxPTP deployment, use the following command:

.. code-block:: bash

    helm uninstall linuxptp -n srsran

To delete the Open5GS deployment, use the following command:

.. code-block:: bash

    helm uninstall open5gs -n open5gs

To delete the Grafana deployment, use the following command:

.. code-block:: bash

    helm uninstall srsran-grafana -n srsran
